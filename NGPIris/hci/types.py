from typing import Required, TypedDict


class TypedResponse(TypedDict, total=False):
    pass


class TypedRequest(TypedDict, total=False):
    pass


class TypedInnerDict(TypedDict, total=False):
    pass


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


class Field(TypedInnerDict):
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


class IndexResponse(TypedResponse):
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


class FacetRequest(TypedInnerDict):
    modelVersion: str
    fieldName: str
    minCount: int
    maxCount: int
    termFilters: list[str]
    facetPrefix: str


class SortField(TypedInnerDict):
    modelVersion: str
    sortField: str
    sortOrder: str


class FilterQueries(TypedInnerDict):
    modelVersion: str
    queryString: str


class CustomParameters(TypedInnerDict):
    modelVersion: str
    name: str
    value: str


class QueryRequest(TypedRequest):
    modelVersion: str
    indexName: str
    queryString: str
    offset: int
    itemsToReturn: int
    facetRequests: list[FacetRequest]
    sortFields: list[SortField]
    filterQueries: list[FilterQueries]
    customParameters: list[CustomParameters]
    returnedFieldFilter: list[str]
