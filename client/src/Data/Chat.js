export const BOT = "BOT_CHAT";
export const USER = "USER_CHAT";
export const IMAGE = "IMAGE_CHAT";
export const TEXT = "TEXT_CHAT";
export const CHECK = "CHECK_CHAT";
export const INFO = "INFO_CHAT";
export const LOADING = "LOADING_CHAT";

export const objectsList = [
  "Bird",
  "Cat",
  "Cow",
  "Dog",
  "Sheep",
  "Horse",
  "Person",
];

export const chat = [
  {
    user: BOT,
    type: IMAGE,
  },
  {
    user: BOT,
    type: TEXT,
    text: "Left Message",
  },
  {
    user: BOT,
    type: CHECK,
    list: "all_parts",
    title: "Select Parts that you want in Image -",
  },
  {
    user: USER,
    type: TEXT,
    text: "Right Message",
  },
  {
    user: INFO,
    type: TEXT,
    text: "Center Message",
  },
  {
    user: LOADING,
    type: TEXT,
    text: "Generating",
  },
];

export const updateObjectList = [
  "Edit Part Bounding Boxes",
  "Edit Part Masks",
  "Generate Another Image",
  "Start Over",
];

export const all_parts = [
  { part: "head", full_part: "Head" },
  { part: "leye", full_part: "Left Eye" },
  { part: "reye", full_part: "Right Eye" },
  { part: "lear", full_part: "Left Ear" },
  { part: "rear", full_part: "Right Ear" },
  { part: "muzzle", full_part: "Muzzle" },
  { part: "lhorn", full_part: "Left Horn" },
  { part: "rhorn", full_part: "Right Horn" },
  { part: "torso", full_part: "Torso" },
  { part: "neck", full_part: "Neck" },
  { part: "lfuleg", full_part: "Left Leg" },
  { part: "lflleg", full_part: "Left Leg" },
  { part: "rfuleg", full_part: "Right Leg" },
  { part: "rflleg", full_part: "Right Leg" },
  { part: "lbuleg", full_part: "Left Leg" },
  { part: "lblleg", full_part: "Left Leg" },
  { part: "rbuleg", full_part: "Right Leg" },
  { part: "rblleg", full_part: "Right Leg" },
  { part: "tail", full_part: "Tail" },
];

export const generationProcessList = ["Random Parts", "Specific Parts"];

export const colorsList = [
  "#ff0000",
  "#bb8f8f",
  "#4169e0",
  "#8a4512",
  "#f98071",
  "#f9a35f",
  "#2d8a56",
  "#800080",
  "#9f522c",
  "#c0c0c0",
  "#86ceeb",
  "#6a5acd",
  "#6f8090",
  "#c74d90",
  "#dd9fdd",
  "#00ff7e",
  "#4682b4",
  "#d2b48b",
  "#008080",
  "#d7bed7",
  "#ff6246",
  "#40dfd0",
  "#ed82ed",
  "#f5deb3",
];
