"""Test waldiez.exporting.agents.rag_user.pgvector_utils.*."""

from waldiez.exporting.agents.rag_user.pgvector_utils import (
    get_pgvector_db_args,
)
from waldiez.models import (
    WaldiezRagUser,
    WaldiezRagUserData,
    WaldiezRagUserRetrieveConfig,
    WaldiezRagUserVectorDbConfig,
)

# pylint: disable=line-too-long


def test_get_pgvector_db_args() -> None:
    """Test get_pgvector_db_args."""
    # Given
    rag_user = WaldiezRagUser(
        id="wa-1",
        type="agent",
        name="rag_user",
        description="description",
        agent_type="rag_user",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        data=WaldiezRagUserData(  # type: ignore
            retrieve_config=WaldiezRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                vector_db="pgvector",
                db_config=WaldiezRagUserVectorDbConfig(  # type: ignore
                    connection_url="http://localhost:5432",
                    use_local_storage=True,
                    local_storage_path="local_storage_path",
                    model="model",
                ),
                use_custom_embedding=False,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    kwargs, imports, embeddings_func = get_pgvector_db_args(
        rag_user, agent_name
    )
    # Then
    assert kwargs == (
        '            client=psycopg.connect("http://localhost:5432"),\n'
        '            embedding_function=SentenceTransformer("model").encode,\n'
    )
    assert imports == {
        "psycopg",
        "from sentence_transformers import SentenceTransformer",
    }
    assert embeddings_func == ""


def test_get_pgvector_db_args_custom_embeddings() -> None:
    """Test get_pgvector_db_args with custom embeddings."""
    # Given
    custom_embedding = (
        "def custom_embedding_function():\n"
        '    return SentenceTransformer("model").encode\n'
    )
    rag_user = WaldiezRagUser(
        id="wa-1",
        type="agent",
        name="rag_user",
        description="description",
        agent_type="rag_user",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        data=WaldiezRagUserData(  # type: ignore
            retrieve_config=WaldiezRagUserRetrieveConfig(  # type: ignore
                docs_path="docs_path",
                collection_name="collection_name",
                vector_db="pgvector",
                db_config=WaldiezRagUserVectorDbConfig(  # type: ignore
                    connection_url="http://localhost:5432",
                    use_local_storage=True,
                    local_storage_path="local_storage_path",
                    model="model",
                ),
                use_custom_embedding=True,
                embedding_function=custom_embedding,
            ),
        ),
    )
    agent_name = "rag_user"
    # When
    kwargs, imports, embeddings_func = get_pgvector_db_args(
        rag_user, agent_name
    )
    # Then
    assert kwargs == (
        '            client=psycopg.connect("http://localhost:5432"),\n'
        "            embedding_function=custom_embedding_function_rag_user,\n"
    )
    assert imports == {
        "psycopg",
    }
    assert embeddings_func == (
        "\ndef custom_embedding_function_rag_user():\n"
        "    # type: () -> Callable[..., Any]\n"
        '    return SentenceTransformer("model").encode\n'
    )