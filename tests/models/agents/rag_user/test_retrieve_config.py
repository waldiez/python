"""Test waldiez.models.agents.rag_user.retrieve_config.*."""

# flake8: noqa E501
import os
import shutil
from pathlib import Path

import pytest

from waldiez.models.agents.rag_user.retrieve_config import (
    WaldiezRagUserRetrieveConfig,
)
from waldiez.models.agents.rag_user.vector_db_config import (
    WaldiezRagUserVectorDbConfig,
)


def test_waldiez_rag_user_retrieve_config() -> None:
    """Test WaldiezRagUserRetrieveConfig."""
    retrieve_config = WaldiezRagUserRetrieveConfig(
        task="default",
        vector_db="chroma",
        db_config=WaldiezRagUserVectorDbConfig(
            model="all-MiniLM-L6-v2",
            use_memory=True,
            use_local_storage=False,
            local_storage_path=None,
            connection_url=None,
            wait_until_index_ready=None,
            wait_until_document_ready=None,
            metadata={},
        ),
        docs_path="folder",
        new_docs=True,
        model=None,
        chunk_token_size=None,
        context_max_tokens=None,
        chunk_mode="multi_lines",
        must_break_at_empty_line=True,
        use_custom_embedding=False,
        embedding_function=None,
        customized_prompt=None,
        customized_answer_prefix="",
        update_context=True,
        collection_name="autogen-docs",
        get_or_create=False,
        overwrite=False,
        use_custom_token_count=False,
        custom_token_count_function=None,
        use_custom_text_split=False,
        custom_text_split_function=None,
        custom_text_types=None,
        recursive=False,
        distance_threshold=-1.0,
        n_results=-1,
    )
    assert retrieve_config.embedding_function_string is None
    assert retrieve_config.text_split_function_string is None
    assert retrieve_config.token_count_function_string is None


def test_waldiez_rag_user_retrieve_config_custom_embedding() -> None:
    """Test WaldiezRagUserRetrieveConfig with custom embedding."""
    embedding_function = """
def custom_embedding_function():
    return list
"""
    retrieve_config = WaldiezRagUserRetrieveConfig(  # type: ignore
        use_custom_embedding=True,
        embedding_function=embedding_function,
    )
    assert retrieve_config.embedding_function_string is not None
    assert (
        retrieve_config.embedding_function_string
        == "    # type: () -> Callable[..., Any]\n    return list"
    )
    assert retrieve_config.text_split_function_string is None
    assert retrieve_config.token_count_function_string is None

    with pytest.raises(ValueError):
        WaldiezRagUserRetrieveConfig(  # type: ignore
            use_custom_embedding=True,
            embedding_function=None,
        )

    with pytest.raises(ValueError):
        WaldiezRagUserRetrieveConfig(  # type: ignore
            use_custom_embedding=True,
            embedding_function="def something():\n   return list",
        )


def test_waldiez_rag_user_retrieve_config_custom_token_count() -> None:
    """Test WaldiezRagUserRetrieveConfig with custom token count."""
    token_count_function = """
def custom_token_count_function(text, model):
    return 0
"""  # nosemgrep # nosec
    retrieve_config = WaldiezRagUserRetrieveConfig(  # type: ignore
        use_custom_token_count=True,
        custom_token_count_function=token_count_function,
    )
    assert retrieve_config.token_count_function_string is not None
    assert (
        retrieve_config.token_count_function_string
        == "    # type: (str, str) -> int\n    return 0"  # nosemgrep # nosec
    )
    assert retrieve_config.embedding_function_string is None
    assert retrieve_config.text_split_function_string is None

    with pytest.raises(ValueError):
        WaldiezRagUserRetrieveConfig(  # type: ignore
            use_custom_token_count=True,
            custom_token_count_function=None,
        )

    with pytest.raises(ValueError):
        WaldiezRagUserRetrieveConfig(  # type: ignore  # nosemgrep # nosec
            use_custom_token_count=True,
            custom_token_count_function="def something():\n    return 0",
        )


# pylint: disable=line-too-long
def test_waldiez_rag_user_retrieve_config_custom_text_split() -> None:
    """Test WaldiezRagUserRetrieveConfig with custom text split."""
    text_split_function = """
def custom_text_split_function(text, max_tokens, chunk_mode, must_break_at_empty_line, overlap):
    return [text]
"""
    retrieve_config = WaldiezRagUserRetrieveConfig(  # type: ignore
        use_custom_text_split=True,
        custom_text_split_function=text_split_function,
    )
    assert retrieve_config.text_split_function_string is not None
    assert (
        retrieve_config.text_split_function_string
        == "    # type: (str, int, str, bool, int) -> List[str]\n    return [text]"
    )
    assert retrieve_config.embedding_function_string is None
    assert retrieve_config.token_count_function_string is None

    with pytest.raises(ValueError):
        WaldiezRagUserRetrieveConfig(  # type: ignore
            use_custom_text_split=True,
            custom_text_split_function=None,
        )

    with pytest.raises(ValueError):
        WaldiezRagUserRetrieveConfig(  # type: ignore
            use_custom_text_split=True,
            custom_text_split_function="def something():\n    return []",
        )


def test_not_resolved_path() -> None:
    """Test not resolved path."""
    with pytest.raises(ValueError):
        WaldiezRagUserRetrieveConfig(  # type: ignore
            task="default",
            vector_db="chroma",
            docs_path="/path/to/not_resolved_path.txt",
        )


def test_with_file_as_doc_path(tmp_path: Path) -> None:
    """Test with file as doc path (resolved).

    Parameters
    ----------
    tmp_path : Path
        The temporary path.
    """
    docs_file = tmp_path / "test_with_file_as_doc_path.txt"
    docs_file.touch()
    config = WaldiezRagUserRetrieveConfig(  # type: ignore
        task="default",
        vector_db="chroma",
        docs_path=[str(docs_file)],
    )
    assert config.docs_path == [f'r"{docs_file}"']
    docs_file.unlink()


def test_with_folder_as_doc_path(tmp_path: Path) -> None:
    """Test with folder as doc path.

    Parameters
    ----------
    tmp_path : Path
        The temporary path.
    """
    # not ending with os.sep (we check if is_dir)
    docs_dir = tmp_path / "test_with_folder_as_doc_path"
    docs_dir.mkdir(exist_ok=True)
    config = WaldiezRagUserRetrieveConfig(  # type: ignore
        task="default",
        vector_db="chroma",
        docs_path=[str(docs_dir)],
    )
    assert config.docs_path == [f'r"{docs_dir}"']
    shutil.rmtree(docs_dir, ignore_errors=True)
    # ending with os.sep we assume it is a folder
    docs_dir.mkdir(exist_ok=True)
    doc_path = str(docs_dir) + os.path.sep
    config = WaldiezRagUserRetrieveConfig(  # type: ignore
        task="default",
        vector_db="chroma",
        docs_path=[doc_path],
    )
    assert config.docs_path == [f'r"{doc_path}"']
    shutil.rmtree(docs_dir, ignore_errors=True)
