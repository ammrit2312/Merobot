const initialState = { rect_image: "", mask_image: "", generated_image: "" };

export const getImage = (images) => {
  return {
    type: "GET_IMAGE",
    images,
  };
};

export const ImageStore = (state = initialState, action) => {
  switch (action.type) {
    case "GET_IMAGE":
      return {
        ...state,
        rect_image: action.images[0],
        mask_image: action.images[1],
        generated_image: action.images[2],
      };
    default:
      return state;
  }
};
