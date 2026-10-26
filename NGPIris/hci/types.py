from typing import Literal, Required, TypedDict

query_response = {
    "modelVersion": str,
    "indexName": str,
    "indexDisplayName": str,
    "results": [
        {
            "metadata": {
                "additionalProp1": [str],
                "additionalProp2": [str],
                "additionalProp3": [str],
            },
            "relevance": int,
            "modelVersion": str,
            "id": str,
            "title": str,
            "link": str,
            "displayFields": [
                {
                    "modelVersion": str,
                    "name": str,
                    "type": "TITLE, TITLE_ICON, LINK, SNIPPET, METADATA, LABELED_METADATA, IMAGE, AUDIO, VIDEO, HTML, DOCUMENT_METADATA",
                    "value": str,
                    "options": [
                        {
                            "modelVersion": str,
                            "name": "HIGHLIGHT, HIDE_FIELD_IF_NO_HIGHLIGHT, FULL_TEXT_HIGHLIGHT, EXPANDABLE",
                            "value": str,
                        }
                    ],
                }
            ],
        }
    ],
    "facets": [
        {
            "modelVersion": str,
            "fieldName": str,
            "displayName": str,
            "termCounts": [{"modelVersion": str, "term": str, "count": int}],
        }
    ],
    "hitCount": int,
    "jsonFacets": str,
    "showHciID": bool,
}


class Field(TypedDict, total=False):
    """
    A typed dictionary for modeling a field in the HCI.
    """

    modelVersion: str
    name: Required[str]
    type: Required[str]
    displayName: str
    sortable: Required[bool]
    filterable: Required[bool]
    defaultFilter: Required[bool]
    facetable: Required[bool]
    facetMinCount: int
    facetMaxCount: int


class IndexResponse(TypedDict, total=False):
    """
    A typed dictionary based on HCI Search API docs.
    """

    modelVersion: str
    name: Required[str]
    displayName: str
    fields: Required[list[Field]]
    displayTitleFieldint: str
    intdisplayLinkFieldint: str
    intdisplayPreviewTextFieldsint: list[str]
    intdisplayCustomFieldsint: list[str]
    intautocompleteint: bool
    intvisualizationsint: bool
    intdownloadResultsint: bool
    intqueryParametersint: bool
    intfieldSelectionint: bool
    intpluginNameint: str
    intbulkActionsint: bool
    intshowHciIDint: bool


class FacetRequest(TypedDict, total=False):
    modelVersion: str
    fieldName: Required[str]
    minCount: int
    maxCount: int
    termFilters: list[str]
    facetPrefix: str


class SortField(TypedDict, total=False):
    modelVersion: str
    sortField: Required[str]
    sortOrder: Required[str]


class FilterQueries(TypedDict, total=False):
    modelVersion: str
    queryString: Required[str]


class CustomParameters(TypedDict, total=False):
    modelVersion: str
    name: Required[str]
    value: Required[str]


class QueryRequest(TypedDict, total=False):
    modelVersion: str
    indexName: Required[str]
    queryString: str
    offset: int
    itemsToReturn: int
    facetRequests: list[FacetRequest]
    sortFields: list[SortField]
    filterQueries: list[FilterQueries]
    customParameters: list[CustomParameters]
    returnedFieldFilter: list[str]


class Metadata(TypedDict, total=False, extra_items=list[str]):
    """
    The keys of dictionary is entirely depandant on the content of the index,
    but each key will always have a value of type :py:type:`list[str]`.
    """


class Options(TypedDict, total=False):
    modelVersion: str
    name: Required[
        Literal[
            "HIGHLIGHT",
            "HIDE_FIELD_IF_NO_HIGHLIGHT",
            "FULL_TEXT_HIGHLIGHT",
            "EXPANDABLE",
        ]
    ]
    value: Required[str]


class DisplayField(TypedDict, total=False):
    modelVersion: str
    name: Required[str]
    type: Required[
        Literal[
            "TITLE",
            "TITLE_ICON",
            "LINK",
            "SNIPPET",
            "METADATA",
            "LABELED_METADATA",
            "IMAGE",
            "AUDIO",
            "VIDEO",
            "HTML",
            "DOCUMENT_METADATA",
        ]
    ]
    value: str
    options: list[Options]


class Result(TypedDict, total=False):
    metadata: Metadata
    relevance: float
    modelVersion: str
    id: str
    title: str
    link: str
    displayFields: Required[list[DisplayField]]


class TermCount(TypedDict, total=False):
    modelVersion: str
    term: Required[str]
    count: int


class Facet(TypedDict, total=False):
    modelVersion: str
    fieldName: Required[str]
    displayName: str
    termCounts: Required[list[TermCount]]


class QueryResponse(TypedDict, total=False):
    modelVersion: str
    indexName: Required[str]
    indexDisplayName: str
    results: Required[list[Result]]
    facets: list[Facet]
    hitCount: Required[int]
    jsonFacets: str
    showHciID: bool
