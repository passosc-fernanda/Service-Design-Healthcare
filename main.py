"""
This script runs a fully automated AI workflow integrated with Notion.

It continuously monitors a Notion database for pages marked with a
"run_ai" checkbox. When a page is flagged, the script retrieves the
corresponding question, gathers contextual summaries from other pages
in the database, and sends this information to the OpenAI API to generate
a contextualized answer.

The generated answer is then written back to the same Notion page, and
the "run_ai" flag is automatically cleared to prevent duplicate runs.

This enables a one-click AI interaction directly from the Notion
interface, without requiring manual execution or a command-line
interaction.
"""

import time
from notion_reader import (
    get_pages_and_summaries,
    get_questions_to_answer,
    write_answer_property,
    clear_run_ai
)
from ai import ask_ai


def run():
    pages = get_pages_and_summaries()

    while True:
        tasks = get_questions_to_answer()

        if tasks:
            for task in tasks:
                answer = ask_ai(
                    question=task["question"],
                    summaries=[p["summary"] for p in pages]
                )

                write_answer_property(task["page_id"], answer)
                clear_run_ai(task["page_id"])

        time.sleep(5)


if __name__ == "__main__":
    run()
