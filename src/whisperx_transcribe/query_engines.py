import logging
from typing import Tuple

from llama_index.core import SummaryIndex
from llama_index.core.prompts import RichPromptTemplate
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.vector_stores import (
    ExactMatchFilter,
    MetadataFilters,
)


def query_per_speaker(
    summary_index: SummaryIndex, speaker: str
) -> Tuple[RetrieverQueryEngine, QueryEngineTool]:
    """Prepare a query engine using the for a specific speaker."""
    template_var_mappings = {
        "speaker": speaker,
        # context_str mapping is done internally
    }
    base = RichPromptTemplate(
        template_str=open("../prompts/speaker_summary_01.md", "r").read(),
        template_format="f-string",
        template_var_mappings=template_var_mappings,
    )
    # to filer the query engine
    filters = MetadataFilters(
        filters=[ExactMatchFilter(key="speaker", value=speaker)]
    )
    query_engine = summary_index.as_query_engine(
        summary_template=base,
        response_mode="tree_summarize",
        filters=filters,
    )
    logging.info(
        "Prompt for query_per_speaker where speaker is"
        f"{speaker}: {query_engine.get_prompts()}"
    )
    summary_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        description=(
            "Useful for finding the main topics addressed ONLY by the"
            f"speaker identified as {speaker}"
        ),
    )

    return query_engine, summary_tool


def query_action_items(
    summary_index: SummaryIndex,
) -> Tuple[RetrieverQueryEngine, QueryEngineTool]:
    base = RichPromptTemplate(
        template_str=open("../prompts/conv_action_items_01.md", "r").read(),
        template_format="f-string",
    )
    query_engine = summary_index.as_query_engine(
        summary_template=base,
        response_mode="tree_summarize",
    )
    action_items_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        description=(
            "Useful for identifying the main action items based on the "
            "full conversation provided."
        ),
    )
    return query_engine, action_items_tool


def query_disagreements(
    summary_index: SummaryIndex,
) -> Tuple[RetrieverQueryEngine, QueryEngineTool]:
    base = RichPromptTemplate(
        template_str=open("../prompts/conv_disagreements_01.md", "r").read(),
        template_format="f-string",
    )
    query_engine = summary_index.as_query_engine(
        summary_template=base,
        response_mode="tree_summarize",
    )
    disagreements_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        description=(
            "Useful for identifying the any disagreements debates or "
            "unresolved items based on the full conversation provided."
        ),
    )
    return query_engine, disagreements_tool


def query_key_decisions(
    summary_index: SummaryIndex,
) -> Tuple[RetrieverQueryEngine, QueryEngineTool]:
    base = RichPromptTemplate(
        template_str=open("../prompts/conv_key_decisions_01.md", "r").read(),
        template_format="f-string",
    )
    query_engine = summary_index.as_query_engine(
        summary_template=base,
        response_mode="tree_summarize",
    )
    decisions_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        description=(
            "Useful for identifying all key decisions and conclusions"
            "reached based on the full conversation provided."
        ),
    )
    return query_engine, decisions_tool


def query_key_items(
    summary_index: SummaryIndex,
) -> Tuple[RetrieverQueryEngine, QueryEngineTool]:
    base = RichPromptTemplate(
        template_str=open("../prompts/conv_key_items_01.md", "r").read(),
        template_format="f-string",
    )
    query_engine = summary_index.as_query_engine(
        summary_template=base,
        response_mode="tree_summarize",
    )
    key_items_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        description=(
            "Useful for identifying the primary topics or agenda"
            "items based on the full conversation provided."
        ),
    )
    return query_engine, key_items_tool


def query_tldr(
    summary_index: SummaryIndex,
) -> Tuple[RetrieverQueryEngine, QueryEngineTool]:
    base = RichPromptTemplate(
        template_str=open("../prompts/conv_tldr_01.md", "r").read(),
        template_format="f-string",
    )
    query_engine = summary_index.as_query_engine(
        summary_template=base,
        response_mode="tree_summarize",
    )
    tldr_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        description=(
            "Useful for generating a concise summary (TLDR) of the meeting's "
            "most important takeaways based on the full conversation provided."
        ),
    )
    return query_engine, tldr_tool
