# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Load data from dataframes into collections of data objects."""

import pandas as pd

from graphrag.data_model.community import Community
from graphrag.data_model.community_report import CommunityReport
from graphrag.data_model.covariate import Covariate
from graphrag.data_model.entity import Entity
from graphrag.data_model.relationship import Relationship
from graphrag.data_model.text_unit import TextUnit
from graphrag.query.input.loaders.utils import (
    to_list,
    to_optional_dict,
    to_optional_float,
    to_optional_int,
    to_optional_list,
    to_optional_str,
    to_str,
)


def _prepare_records(df: pd.DataFrame) -> list[dict]:
    """
    Reset index and convert the DataFrame to a list of dictionaries.

    We rename the reset index column to 'Index' for consistency.
    """
    df_reset = df.reset_index().rename(columns={"index": "Index"})
    return df_reset.to_dict("records")


def read_entities(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: str | None = "human_readable_id",
    title_col: str = "title",
    type_col: str | None = "type",
    description_col: str | None = "description",
    name_embedding_col: str | None = "name_embedding",
    description_embedding_col: str | None = "description_embedding",
    community_col: str | None = "community_ids",
    text_unit_ids_col: str | None = "text_unit_ids",
    rank_col: str | None = "degree",
    attributes_cols: list[str] | None = None,
) -> list[Entity]:
    """Read entities from a dataframe using pre-converted records."""
    records = _prepare_records(df)
    return [
        Entity(
            id=to_str(row, id_col),
            short_id=to_optional_str(row, short_id_col)
            if short_id_col
            else str(row["Index"]),
            title=to_str(row, title_col),
            type=to_optional_str(row, type_col),
            description=to_optional_str(row, description_col),
            name_embedding=to_optional_list(row, name_embedding_col, item_type=float),
            description_embedding=to_optional_list(
                row, description_embedding_col, item_type=float
            ),
            community_ids=to_optional_list(row, community_col, item_type=str),
            text_unit_ids=to_optional_list(row, text_unit_ids_col),
            rank=to_optional_int(row, rank_col),
            attributes=(
                {col: row.get(col) for col in attributes_cols}
                if attributes_cols
                else None
            ),
        )
        for row in records
    ]


def read_relationships(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: str | None = "human_readable_id",
    source_col: str = "source",
    target_col: str = "target",
    description_col: str | None = "description",
    rank_col: str | None = "combined_degree",
    description_embedding_col: str | None = "description_embedding",
    weight_col: str | None = "weight",
    text_unit_ids_col: str | None = "text_unit_ids",
    attributes_cols: list[str] | None = None,
) -> list[Relationship]:
    """Read relationships from a dataframe using pre-converted records."""
    records = _prepare_records(df)
    return [
        Relationship(
            id=to_str(row, id_col),
            short_id=to_optional_str(row, short_id_col)
            if short_id_col
            else str(row["Index"]),
            source=to_str(row, source_col),
            target=to_str(row, target_col),
            description=to_optional_str(row, description_col),
            description_embedding=to_optional_list(
                row, description_embedding_col, item_type=float
            ),
            weight=to_optional_float(row, weight_col),
            text_unit_ids=to_optional_list(row, text_unit_ids_col, item_type=str),
            rank=to_optional_int(row, rank_col),
            attributes=(
                {col: row.get(col) for col in attributes_cols}
                if attributes_cols
                else None
            ),
        )
        for row in records
    ]


def read_covariates(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: str | None = "human_readable_id",
    subject_col: str = "subject_id",
    covariate_type_col: str | None = "type",
    text_unit_ids_col: str | None = "text_unit_ids",
    attributes_cols: list[str] | None = None,
) -> list[Covariate]:
    """Read covariates from a dataframe using pre-converted records."""
    records = _prepare_records(df)
    return [
        Covariate(
            id=to_str(row, id_col),
            short_id=to_optional_str(row, short_id_col)
            if short_id_col
            else str(row["Index"]),
            subject_id=to_str(row, subject_col),
            covariate_type=(
                to_str(row, covariate_type_col) if covariate_type_col else "claim"
            ),
            text_unit_ids=to_optional_list(row, text_unit_ids_col, item_type=str),
            attributes=(
                {col: row.get(col) for col in attributes_cols}
                if attributes_cols
                else None
            ),
        )
        for row in records
    ]


def read_communities(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: str | None = "community",
    title_col: str = "title",
    level_col: str = "level",
    entities_col: str | None = "entity_ids",
    relationships_col: str | None = "relationship_ids",
    covariates_col: str | None = "covariate_ids",
    parent_col: str | None = "parent",
    children_col: str | None = "children",
    attributes_cols: list[str] | None = None,
) -> list[Community]:
    """Read communities from a dataframe using pre-converted records."""
    records = _prepare_records(df)
    return [
        Community(
            id=to_str(row, id_col),
            short_id=to_optional_str(row, short_id_col)
            if short_id_col
            else str(row["Index"]),
            title=to_str(row, title_col),
            level=to_str(row, level_col),
            entity_ids=to_optional_list(row, entities_col, item_type=str),
            relationship_ids=to_optional_list(row, relationships_col, item_type=str),
            covariate_ids=to_optional_dict(
                row, covariates_col, key_type=str, value_type=str
            ),
            parent=to_str(row, parent_col),
            children=to_list(row, children_col),
            attributes=(
                {col: row.get(col) for col in attributes_cols}
                if attributes_cols
                else None
            ),
        )
        for row in records
    ]


def read_community_reports(
    df: pd.DataFrame,
    id_col: str = "id",
    short_id_col: str | None = "community",
    title_col: str = "title",
    community_col: str = "community",
    summary_col: str = "summary",
    content_col: str = "full_content",
    rank_col: str | None = "rank",
    content_embedding_col: str | None = "full_content_embedding",
    attributes_cols: list[str] | None = None,
) -> list[CommunityReport]:
    """Read community reports from a dataframe using pre-converted records."""
    records = _prepare_records(df)
    return [
        CommunityReport(
            id=to_str(row, id_col),
            short_id=to_optional_str(row, short_id_col)
            if short_id_col
            else str(row["Index"]),
            title=to_str(row, title_col),
            community_id=to_str(row, community_col),
            summary=to_str(row, summary_col),
            full_content=to_str(row, content_col),
            rank=to_optional_float(row, rank_col),
            full_content_embedding=to_optional_list(
                row, content_embedding_col, item_type=float
            ),
            attributes=(
                {col: row.get(col) for col in attributes_cols}
                if attributes_cols
                else None
            ),
        )
        for row in records
    ]


def read_text_units(
    df: pd.DataFrame,
    id_col: str = "id",
    text_col: str = "text",
    entities_col: str | None = "entity_ids",
    relationships_col: str | None = "relationship_ids",
    covariates_col: str | None = "covariate_ids",
    tokens_col: str | None = "n_tokens",
    document_ids_col: str | None = "document_ids",
    attributes_cols: list[str] | None = ["metadata"],
) -> list[TextUnit]:
    """Read text units from a dataframe using pre-converted records."""
    records = _prepare_records(df)
    return [
        TextUnit(
            id=to_str(row, id_col),
            short_id=str(row["Index"]),
            text=to_str(row, text_col),
            entity_ids=to_optional_list(row, entities_col, item_type=str),
            relationship_ids=to_optional_list(row, relationships_col, item_type=str),
            covariate_ids=to_optional_dict(
                row, covariates_col, key_type=str, value_type=str
            ),
            n_tokens=to_optional_int(row, tokens_col),
            document_ids=to_optional_list(row, document_ids_col, item_type=str),
            attributes=(
                {col: row.get(col) for col in attributes_cols}
                if attributes_cols
                else None
            ),
        )
        for row in records
    ]
