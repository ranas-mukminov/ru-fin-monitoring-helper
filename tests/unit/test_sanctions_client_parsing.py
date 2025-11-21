from sanctions.opensanctions_client.models import Entity, SearchResponse


def test_entity_from_api_payload():
    payload = {
        "id": "os-123",
        "name": "John Doe",
        "datasets": ["sanctions", "pep"],
        "score": 92.5,
    }
    entity = Entity.from_api(payload)
    assert entity.id == "os-123"
    assert entity.name == "John Doe"
    assert "sanctions" in entity.datasets
    assert entity.score == 92.5


def test_search_response_parsing():
    payload = {
        "results": [
            {"id": "os-1", "name": "Alice", "datasets": ["sanctions"], "score": 88},
            {"id": "os-2", "name": "Bob", "datasets": ["pep"], "score": None},
        ]
    }
    response = SearchResponse.from_api(payload)
    assert len(response.results) == 2
    assert response.results[0].name == "Alice"
    assert response.results[1].datasets == ["pep"]
