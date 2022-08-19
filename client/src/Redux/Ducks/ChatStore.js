import { BOT, TEXT, USER, CHECK, LOADING, IMAGE } from "../../Data/Chat";

const initialState = [];

export const botText = (message) => {
  return {
    type: "botText",
    message,
  };
};

export const botImage = (images) => {
  return {
    type: "botImage",
    images,
  };
};

export const userText = (message) => {
  return {
    type: "userText",
    message,
  };
};

export const botCheck = (list, title) => {
  return {
    type: "botCheck",
    list,
    title,
  };
};

export const addLoadingChat = () => {
  return {
    type: "addLoadingChat",
  };
};

export const removeLoadingChat = () => {
  return {
    type: "removeLoadingChat",
  };
};

export const ChatStore = (state = initialState, action) => {
  switch (action.type) {
    case "botText":
      return [
        ...state,
        {
          user: BOT,
          type: TEXT,
          text: action.message,
        },
      ];
    case "userText":
      return [
        ...state,
        {
          user: USER,
          type: TEXT,
          text: action.message,
        },
      ];
    case "botCheck":
      return [
        ...state,
        {
          user: BOT,
          type: CHECK,
          list: action.list,
          title: action.title,
        },
      ];
    case "addLoadingChat":
      return [
        ...state,
        {
          user: LOADING,
          type: TEXT,
        },
      ];
    case "removeLoadingChat":
      return state.filter((item) => item.user !== LOADING);
    case "botImage":
      return [
        ...state,
        {
          user: BOT,
          type: IMAGE,
          rect_image: action.images[0],
          mask_image: action.images[1],
          generated_image: action.images[2],
        },
      ];
    default:
      return state;
  }
};
