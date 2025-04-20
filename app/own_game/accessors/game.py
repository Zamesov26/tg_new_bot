from sqlalchemy import Sequence, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.base.base_accessor import BaseAccessor
from app.bot.game_bot.constants import States
from app.own_game.models.games import Game, Player, QuestionsToGame
from app.own_game.models.questions import Category, Question
from app.own_game.models.users import User


class PriceGenerator:
    def __init__(self, start=100, step=100):
        self.curr = start
        self.step = step

    def __iter__(self):
        while True:
            yield self.curr
            self.curr += self.step


class GameAccessor(BaseAccessor):
    async def get_game_by_id(self, db_session: AsyncSession, game_id):
        stmt = (
            select(Game)
            .where(Game.id == game_id)
            .options(
                selectinload(Game.active_question),
                selectinload(Game.responding_user),
                selectinload(Game.active_user),
            )
            .with_for_update()
        )
        game = await db_session.execute(stmt)
        return game.scalar_one_or_none()

    async def get_games_by_state(self, db_session, state) -> list[Game]:
        stmt = select(Game).where(Game.state == state)
        game = await db_session.execute(stmt)
        return list(game.scalars().all())

    async def get_active_game_in_chat(
        self, db_session: AsyncSession, chat_id
    ) -> Game | None:
        stmt = (
            select(Game)
            .where(Game.chat_id == chat_id, Game.is_active)
            .options(
                selectinload(Game.active_question),
                selectinload(Game.responding_user),
                selectinload(Game.active_user),
            )
            .with_for_update()
        )
        game = await db_session.execute(stmt)
        return game.scalar_one_or_none()

    async def get_active_games(self, db_session: AsyncSession) -> list[Game]:
        stmt = select(Game).where(Game.is_active).with_for_update()
        res = await db_session.execute(stmt)
        return list(res.scalars().all())

    async def get_user_games(
        self, db_session: AsyncSession, user_id: int
    ) -> list[Game]:
        stmt = (
            select(Game)
            .join(Player, Player.game_id == Game.id)
            .where(Player.user_id == user_id, Player.is_active)
            .distinct()
        )
        res = await db_session.execute(stmt)
        return list(res.scalars().all())

    async def get_ended_games(self, db_session: AsyncSession) -> list[Game]:
        stmt = select(Game).where(Game.state == States.GAME_OVER)
        res = await db_session.execute(stmt)
        return list(res.scalars().all())

    async def get_stopped_games(self, db_session: AsyncSession) -> list[Game]:
        stmt = select(Game).where(Game.state == States.GAME_STOPPED)
        res = await db_session.execute(stmt)
        return list(res.scalars().all())

    async def close_active_games(self, db_session: AsyncSession, chat_id):
        stmt = (
            update(Game).where(Game.chat_id == chat_id).values(is_active=False)
        )
        await db_session.execute(stmt)

    async def create_game(
        self, db_session: AsyncSession, chat_id, state=States.PREPARING
    ):
        game = Game(chat_id=chat_id, state=state)
        db_session.add(game)
        await db_session.flush()
        return game

    async def update_game(
        self,
        game_id: int,
        state: int | None = None,
        is_active: int | None = None,
        active_user_id: int | None = None,
        responding_user_id: int | None = None,
        active_question_id: int | None = None,
    ) -> Sequence | None:
        new_values = {}
        if state:
            new_values["state"] = state
        if is_active is False:
            new_values["is_active"] = is_active
        if active_question_id:
            new_values["active_question_id"] = active_question_id
        if active_user_id:
            new_values["active_user_id"] = active_user_id
        if responding_user_id:
            new_values["responding_user_id"] = responding_user_id
        if not state:
            return

        async with self.app.database.session() as session:
            stmt = (
                update(Game)
                .where(Game.is_active, Game.id == game_id)
                .values(**new_values)
            )
            await session.execute(stmt)

    async def get_active_players_in_game(
        self, db_session: AsyncSession, game_id: int
    ):
        stmt = (
            select(User.id, User.name, User.tg_id, Player.points)
            .join(Player, Player.user_id == User.id)
            .join(Game, Game.id == Player.game_id)
            .where(Game.id == game_id, Player.is_active)
            .order_by(Player.points)
        )
        res = await db_session.execute(stmt)
        return list(res.all())

    async def toggle_palayer_in_game(
        self, db_session, game_id, user_id
    ) -> Player | None:
        stmt = select(Player).where(
            Player.game_id == game_id,
            Player.user_id == user_id,
        )
        player = (await db_session.execute(stmt)).scalar_one_or_none()
        if player:
            player.is_active = not player.is_active
            return player

        player = Player(
            user_id=user_id, game_id=game_id, is_active=True, points=0
        )
        db_session.add(player)
        return player

    async def assing_random_themes(
        self, db_session, game_id, theme_cnt=6, question_cnt=3
    ):
        categories = await self.app.store.question.get_random_categoris(
            db_session, theme_cnt
        )
        for category in categories:
            questions = (
                await self.app.store.question.get_random_question_for_category(
                    db_session,
                    category_id=category.id,
                    question_cnt=question_cnt,
                )
            )
            for question, price in zip(
                questions, PriceGenerator(), strict=False
            ):
                db_session.add(
                    QuestionsToGame(
                        question_id=question.id, game_id=game_id, price=price
                    )
                )

    async def get_available_categories_by_game(
        self, db_session: AsyncSession, game_id: int
    ) -> list[Category]:
        stmt = (
            select(Category)
            .join(Question, Question.category_id == Category.id)
            .join(QuestionsToGame, QuestionsToGame.question_id == Question.id)
            .where(
                QuestionsToGame.game_id == game_id, QuestionsToGame.is_available
            )
            .distinct()
        )
        res = await db_session.execute(stmt)
        return list(res.scalars().all())

    async def get_available_questions(
        self, db_session: AsyncSession, game_id: int, category_id: int
    ) -> list[QuestionsToGame]:
        stmt = (
            select(QuestionsToGame)
            .join(Question, Question.id == QuestionsToGame.question_id)
            .join(Category, Category.id == Question.category_id)
            .where(
                QuestionsToGame.is_available,
                QuestionsToGame.game_id == game_id,
                Category.id == category_id,
            )
        )
        res = await db_session.execute(stmt)
        return list(res.scalars().all())

    # async def get_question(self, db_session, question_id) -> Question:
    #     stmt = (
    #         select(Question)
    #         .join(QuestionsToGame, QuestionsToGame.question_id == Question.id)
    #         .where(QuestionsToGame.question_id == question_id)
    #     )
    #
    #     res = await db_session.execute(stmt)
    #     return res.scalar_one()

    async def get_user_in_game(
        self, db_session, game_id, user_tg_id
    ) -> User | None:
        stmt = (
            select(User)
            .join(Player, Player.user_id == User.id)
            .where(User.tg_id == user_tg_id, Player.game_id == game_id)
        )
        res = await db_session.execute(stmt)
        return res.scalar_one_or_none()

    async def update_game_question(
        self,
        db_session: AsyncSession,
        game_id: int,
        question_id: int,
        is_available: bool | None = None,
        end_time: int | None = None,
    ):
        values = {}
        if is_available is False:
            values["is_available"] = is_available
        if end_time:
            values["end_time"] = end_time

        stmt = (
            update(QuestionsToGame)
            .where(
                QuestionsToGame.game_id == game_id,
                QuestionsToGame.question_id == question_id,
            )
            .values(**values)
        )
        await db_session.execute(stmt)

    async def change_user_point_by_user_id(
        self, db_session, game_id, user_id, points
    ):
        stmt = (
            update(Player)
            .values(points=Player.points + points)
            .where(
                Player.game_id == game_id,
                Player.user_id == user_id,
            )
        )
        await db_session.execute(stmt)

    async def change_user_point(
        self, db_session, game_id, user_tg_id, question_id, is_increase
    ):
        stmt = update(Player)
        if is_increase:
            stmt = stmt.values(points=Player.points + QuestionsToGame.price)
        else:
            stmt = stmt.values(points=Player.points - QuestionsToGame.price)

        stmt = (
            stmt.where(Player.game_id == game_id)
            .where(User.id == Player.user_id, User.tg_id == user_tg_id)
            .where(
                QuestionsToGame.game_id == Player.game_id,
                QuestionsToGame.question_id == question_id,
            )
            .where(Question.id == QuestionsToGame.question_id)
        )
        await db_session.execute(stmt)

    async def get_game_question(
        self, db_session: AsyncSession, game_id: int, question_id: int
    ) -> QuestionsToGame | None:
        stmt = (
            select(QuestionsToGame)
            .where(
                QuestionsToGame.is_available,
                QuestionsToGame.game_id == game_id,
                QuestionsToGame.question_id == question_id,
            )
            .with_for_update()
        )
        res = await db_session.execute(stmt)
        return res.scalar_one_or_none()
