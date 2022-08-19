import { createStore, combineReducers } from "redux";
import { ImageStore } from "./Ducks/ImageStore";
import { StepStore } from "./Ducks/StepStore";
import { ChatStore } from "./Ducks/ChatStore";
import { DetailsStore } from "./Ducks/Details";
import { ServerStore } from "./Ducks/ServerStore";
import {LinesStore} from "./Ducks/LinesStore";
import {RectanglesStore} from "./Ducks/RectanglesStore";

const allReducers = combineReducers({
  ImageStore,
  StepStore,
  ChatStore,
  DetailsStore,
  ServerStore,
  Lines : LinesStore,
  Rectangles : RectanglesStore,
});

const store = createStore(
  allReducers,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);

export default store;
