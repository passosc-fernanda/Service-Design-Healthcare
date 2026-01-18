from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


def get_pages_and_summaries():
    response = notion.databases.query(database_id=DATABASE_ID)
    rows = response["results"]

    pages = []

    for row in rows:
        page_id = row["id"]

        # Pega automaticamente a coluna Title (ex: Article)
        title = "Untitled"
        for prop in row["properties"].values():
            if prop["type"] == "title" and prop["title"]:
                title = prop["title"][0]["plain_text"]
                break

        # Lê os blocos da página
        blocks = notion.blocks.children.list(block_id=page_id)["results"]

        text = ""
        started = False

        for block in blocks:
            if block["type"] != "paragraph":
                continue

            rich = block["paragraph"]["rich_text"]
            if not rich:
                continue

            content = "".join(t["plain_text"] for t in rich).strip()

            if content.lower().startswith("link"):
                continue

            if content.lower().startswith("summary"):
                started = True
                continue

            if started:
                text += content + " "

        if text:
            pages.append({
                "page_id": page_id,
                "title": title,
                "summary": text.strip()
            })

    return pages


def get_questions_to_answer():
    response = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "run_ai",
            "checkbox": {"equals": True}
        }
    )

    tasks = []

    for row in response["results"]:
        page_id = row["id"]

        question_prop = row["properties"]["Question"]["rich_text"]
        question = question_prop[0]["plain_text"] if question_prop else None

        if not question:
            continue

        tasks.append({
            "page_id": page_id,
            "question": question
        })

    return tasks


def write_answer_property(page_id, answer):
    notion.pages.update(
        page_id=page_id,
        properties={
            "Answer": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": answer}
                    }
                ]
            },
            "run_ai": {
                "checkbox": False
            }
        }
    )

    def write_answer_property(page_id, answer):
        notion.pages.update(
            page_id=page_id,
            properties={
                "answer": {
                    "rich_text": [
                        {"text": {"content": answer}}
                    ]
                }
            }
        )


def clear_run_ai(page_id):
    notion.pages.update(
        page_id=page_id,
        properties={
            "run_ai": {"checkbox": False}
        }
    )

