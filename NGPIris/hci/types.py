from typing import Required, TypedDict

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
