from utils.db_api.schemas.story import Story, Character, Quest, Task, UsersTask
import asyncio
from utils.db_api.db_gino import db


async def add_story(story_name: str, story_desc: str, teacher_id: int):
    try:
        story = await Story.create(story_name=story_name, story_desc=story_desc, teacher_id=teacher_id)
        return story
    except Exception as e:
        print(f'Сказка не добавлена: {e}')
        return None


async def add_character(name: str, character_desc: str, story_id: int, image_path: str):
    try:
        character = await Character.create(name=name, character_desc=character_desc, story_id=story_id, image_path=image_path)
        return character
    except Exception as e:
        print(f'Персонаж не добавлен: {e}')
        return None


async def add_quest(story_id: int, quest_name: str, quest_theme: str, quest_text: str, character_text: str, character_id: int):
    try:
        quest = await Quest.create(story_id=story_id, quest_name=quest_name, quest_theme=quest_theme, quest_text=quest_text, character_text=character_text, character_id=character_id)
        return quest
    except Exception as e:
        print(f'Квест не добавлен: {e}')
        return None


async def get_character_id_by_story_and_name(story_id: int, name: str):
    try:
        character = await Character.query.where((Character.story_id == story_id) & (Character.name == name)).gino.first()
        return character.id if character else None
    except Exception as e:
        print(f'Персонаж не найден: {e}')
        return None


async def get_story_details(story_id: int):
    try:
        story = await Story.query.where(Story.id == story_id).gino.first()
        if story:
            return {
                'id': story.id,
                'name': story.story_name,
                'description': story.story_desc,
                'teacher_id': story.teacher_id
            }
        return None
    except Exception as e:
        print(f'Сказка не найдена: {e}')
        return None


async def add_task(quest_id: int, content: str, answer: str, task_index: int, task_type: str):
    try:
        task = await Task.create(quests_id=quest_id, content=content, answer=answer, task_index=task_index, task_type=task_type)
        return task
    except Exception as e:
        print(f'Задача не добавлена: {e}')
        return None


async def add_user_task(username: str, story_id: int, correct_tasks: int, not_correct_tasks: int):
    try:
        user_task = await UsersTask.create(username=username, story_id=story_id, correct_tasks=correct_tasks, not_correct_tasks=not_correct_tasks)
        return user_task
    except Exception as e:
        print(f'Запись в таблицу UserTask не добавлена: {e}')
        return None



async def add_story_to_db(story_data: dict, teacher_id: int):
    async with db.transaction():
        # Создание сказки
        db_story = await Story.create(story_name=story_data.full_description, story_desc=story_data.full_description, teacher_id=teacher_id)
        
        # Создание персонажей
        for npc in story_data.npcs:
            await Character.create(name=npc.name, character_desc=npc.character_description, story_id=db_story.id, image_path=npc.image_url)
        
        # Создание квестов и задач
        for quest in story_data.quests:
            db_quest = await Quest.create(story_id=db_story.id, quest_name=quest.description, quest_theme=quest.theme, quest_text=quest.description, character_text=quest.replika, character_id=None)
            
            # Создание задач
            for i, task in enumerate(quest.tasks):
                await Task.create(quests_id=db_quest.id, content=task.task_text, answer=task.right_answer, task_index=i)
