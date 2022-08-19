const initialState = {};

export const setServerData = (data) => {
  return {
    type: "SET_SERVER_DATA",
    data,
  };
};

export const removeRemainingParts = (input_label) => {
  return {
    type: "REMOVE_REMAINING_PARTS",
    input_label,
  }
}

export const addRemainingParts = (input_label) => {
  return {
    type: "ADD_REMAINING_PARTS",
    input_label,
  }
}

export const ServerStore = (state = initialState, action) => {
  switch (action.type) {
    case "SET_SERVER_DATA":
      return {
        ...state,
        masked: action.data.masked,
        rectangle: action.data.rectangle,
        labels_used: action.data.labels_used,
        remaining_parts: action.data.remaining_parts,
      };
    case "REMOVE_REMAINING_PARTS":
      return {
        ...state,
        remaining_parts: state.remaining_parts.filter(part => part.full_part !== action.input_label)
      }
    case "ADD_REMAINING_PARTS":
      return {
        ...state,
        remaining_parts: [...state.remaining_parts, {full_part: action.input_label, part: action.input_label}]
      }
    default:
      return state;
  }
};
