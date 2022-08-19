const initialState = {};

export const setObjectName = (objectName) => {
  return {
    type: "SET_OBJECT_NAME",
    objectName,
  };
};

export const setAllParts = (allParts) => {
  return {
    type: "SET_ALL_PARTS",
    allParts,
  };
};

export const storeSpecificPartsList = (specificPartsList) => {
  return {
    type: "STORE_SPECIFIC_PARTS_LIST",
    specificPartsList,
  };
};

export const DetailsStore = (state = initialState, action) => {
  switch (action.type) {
    case "SET_OBJECT_NAME":
      return {
        ...state,
        objectName: action.objectName,
      };
    case "SET_ALL_PARTS":
      return {
        ...state,
        allParts: action.allParts,
      };
    case "STORE_SPECIFIC_PARTS_LIST":
      return {
        ...state,
        specificPartsList: action.specificPartsList,
      };
    default:
      return state;
  }
};
