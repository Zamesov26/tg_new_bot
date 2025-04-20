from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.own_game.models.games import Game, Player, QuestionsToGame
from app.own_game.models.questions import Question
from app.own_game.models.users import User
from app.store import Store


class TestGameAccessor:
    async def test_table_exists(self, inspect_list_tables: list[str]):
        assert "categories" in inspect_list_tables

    async def test_create_game(
        self, db_sessionmaker: async_sessionmaker[AsyncSession], store: Store
    ) -> None:
        game = await store.game.create_game(1)
        assert isinstance(game, Game)

        async with db_sessionmaker() as session:
            games = list(await session.scalars(select(Game)))

        assert len(games) == 1
        assert games[0].id == game.id
        assert games[0].chat_id == game.chat_id

    async def test_update_game(
        self,
        db_sessionmaker: async_sessionmaker[AsyncSession],
        store: Store,
        game_1: Game,
        user_1: User,
        user_2: User,
        question_1: Question,
    ):
        values = {
            "state": 2,
            "active_user_id": user_1.id,
            "responding_user_id": user_2.id,
            "active_question_id": question_1.id,
            "is_active": False,
        }
        await store.game.update_game(game_1.id, **values)
        async with db_sessionmaker() as session:
            game = await session.scalar(
                select(Game).where(Game.chat_id == game_1.chat_id)
            )
        assert isinstance(game, Game)
        assert game.state == 2
        assert game.active_user_id == user_1.id
        assert game.responding_user_id == user_2.id
        assert game.is_active is False
        # assert game.active_question.title == question_1.id

    async def test_toggle_player(
        self,
        db_sessionmaker: async_sessionmaker[AsyncSession],
        store: Store,
        game_1: Game,
        user_1: User,
    ):
        await store.game.toggle_palayer_in_game(game_1.id, user_1.id)
        async with db_sessionmaker() as session:
            players = list(await session.scalars(select(Player)))
        assert len(players) == 1
        assert players[0].is_active is True

        await store.game.toggle_palayer_in_game(game_1.id, user_1.id)
        async with db_sessionmaker() as session:
            players = list(await session.scalars(select(Player)))
        assert len(players) == 1
        assert players[0].is_active is False

    async def test_get_players_in_game(
        self,
        db_sessionmaker: async_sessionmaker[AsyncSession],
        store: Store,
        game_1: Game,
    ):
        async with db_sessionmaker() as session:
            players = list(await session.scalars(select(Player)))

        assert len(players) == 0
        players = await store.game.get_active_players_in_game(game_1.chat_id)
        assert len(players) == 0

    async def test_close_active_game(
        self,
        db_sessionmaker: async_sessionmaker[AsyncSession],
        store: Store,
        game_1: Game,
    ):
        async with db_sessionmaker() as session:
            games = list(
                await session.scalars(select(Game).where(Game.is_active))
            )

        assert len(games) == 1
        await store.game.close_active_games(game_1.chat_id)
        async with db_sessionmaker() as session:
            games = list(
                await session.scalars(select(Game).where(Game.is_active))
            )
        assert len(games) == 0

    async def test_change_user_point(
        self,
        db_sessionmaker: async_sessionmaker[AsyncSession],
        store: Store,
        game_1: Game,
        user_1: User,
        question_1: Question,
    ):
        player = Player(user_id=user_1.id, game_id=game_1.id)
        game_question = QuestionsToGame(
            question_id=question_1.id, game_id=game_1.id, price=100
        )
        async with db_sessionmaker() as session:
            session.add(player)
            session.add(game_question)
            await session.commit()
        # await store.game.change_user_point(
        #     game_1.id, user_1.tg_id, question_1.id, True
        # )

        async with db_sessionmaker() as session:
            stmt = select(Player).where(
                Player.game_id == game_1.id, Player.user_id == user_1.id
            )
            res = await session.execute(stmt)
            player = res.scalar_one()

        assert player.points == 100
