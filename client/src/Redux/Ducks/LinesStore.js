const SET_LINES = "set_lines";

const initState = {
  line: [],
};

export const setLines = (data) => {
  return {
    type: SET_LINES,
    data,
  };
};

export const LinesStore = (state = initState, action) => {
  switch (action.type) {
    case SET_LINES:
      return { ...state, line: action.data };
    default:
      return state;
  }
};
