from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()


def test_identical_vectors():
    vec = [1.0, 2.0, 3.0]
    result = client.cosine_similarity(vec, vec)
    assert abs(result - 1.0) < 1e-9


def test_orthogonal_vectors():
    result = client.cosine_similarity([1.0, 0.0], [0.0, 1.0])
    assert abs(result - 0.0) < 1e-9


def test_opposite_vectors():
    result = client.cosine_similarity([1.0, 2.0], [-1.0, -2.0])
    assert abs(result - (-1.0)) < 1e-9


def test_different_vectors():
    result = client.cosine_similarity([1.0, 2.0, 3.0], [2.0, 3.0, 4.0])
    assert -1.0 <= result <= 1.0
    assert result > 0.9