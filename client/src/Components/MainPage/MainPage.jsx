import React, { useEffect, useRef } from "react";
import styles from "./MainPage.module.css";
import {
  BOT,
  TEXT,
  IMAGE,
  USER,
  generationProcessList,
  objectsList,
  updateObjectList,
  INFO,
} from "../../Data/Chat";
import { useDispatch, useSelector } from "react-redux";
import { FormLabel, Checkbox, Button, TextField } from "@mui/material";
import Autocomplete from "@mui/material/Autocomplete";
import { setStep } from "../../Redux/Ducks/StepStore";
import axios from "axios";
import { baseUrl } from "../../config";
import {
  botText,
  userText,
  botCheck,
  addLoadingChat,
  removeLoadingChat,
  botImage,
} from "../../Redux/Ducks/ChatStore";
import {
  setObjectName,
  setAllParts,
  storeSpecificPartsList,
} from "../../Redux/Ducks/Details";
import { getImage } from "../../Redux/Ducks/ImageStore";
import { ServerStore, setServerData } from "../../Redux/Ducks/ServerStore";
import LineCanvasModal from "../LineCanvasModal/LineCanvasModal";
import { setRectangles } from "../../Redux/Ducks/RectanglesStore";
import { setLines } from "../../Redux/Ducks/LinesStore";
import RectangleCanvasModal from "../RectangleCanvasModal/RectangleCanvasModal";

export default function MainPage() {
  const imageStore = useSelector((state) => state.ImageStore);
  const stepStore = useSelector((state) => state.StepStore);
  const chat = useSelector((state) => state.ChatStore);
  const all_parts = useSelector((state) => state.DetailsStore.allParts);
  const objectName = useSelector((state) => state.DetailsStore.objectName);
  const lines = useSelector((state) => state.Lines.line);
  const rectangles = useSelector((state) => state.Rectangles.rect);
  const serverStore = useSelector((state) => state.ServerStore);

  const [disableCheckBox, setDisableCheckBox] = React.useState(false);
  const [disableInput, setDisableInput] = React.useState(false);
  const [specificPartsList, setSpecificPartsList] = React.useState([]);
  const [state, setState] = React.useState("");
  const [showModal, setShowModal] = React.useState("");

  const dispatch = useDispatch();
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current.scrollTop = chatRef.current.scrollHeight;
  });

  const getAllParts = () => {
    dispatch(addLoadingChat());
    axios
      .get(`${baseUrl}${objectName}/parts`)
      .then((response) => {
        console.log(response);
        dispatch(removeLoadingChat());
        dispatch(setAllParts(response.data.parts));
        dispatch(
          botCheck("all_parts", "Select Parts that you want in Image -")
        );
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const getAllPartsForRandom = () => {
    axios
      .get(`${baseUrl}${objectName}/parts`)
      .then((response) => {
        console.log(response);
        dispatch(setAllParts(response.data.parts));
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const generateImageAPI = (specificPartsList, method) => {
    dispatch(addLoadingChat());
    setDisableInput(true);
    if (method === "specific") {
      axios
        .post(`${baseUrl}${objectName}/specific`, { parts: specificPartsList })
        .then((response) => {
          console.log(response.data);
          dispatch(removeLoadingChat());
          dispatch(getImage(response.data.images));
          dispatch(setServerData(response.data));
          dispatch(setRectangles(response.data.rectangle));
          dispatch(setLines(response.data.masked));
          dispatch(botImage(response.data.images));
          dispatch(botText("What would you like to do next ?"));
          setDisableInput(false);
        });
    } else {
      axios
        .post(`${baseUrl}${objectName}/random`, {
          parts: specificPartsList,
        })
        .then((response) => {
          console.log(response.data);
          dispatch(removeLoadingChat());
          dispatch(getImage(response.data.images));
          dispatch(setServerData(response.data));
          dispatch(setRectangles(response.data.rectangle));
          dispatch(setLines(response.data.masked));
          dispatch(botImage(response.data.images));
          dispatch(botText("What would you like to do next ?"));
          setDisableInput(false);
        });
    }
  };

  const handleSpecificPartsList = (e) => {
    e.preventDefault();
    setDisableCheckBox(!disableCheckBox);
    const parts = e.target;
    const length = parts.length;
    var list = [];
    for (let i = 0; i < length; i++) {
      const part = parts[i];
      if (part.checked) {
        list.push(part.name);
      }
    }
    setSpecificPartsList(list);
    dispatch(storeSpecificPartsList(list));
    generateImageAPI(list, "specific");
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (stepStore.currentStep === 1) {
      if (state !== "") {
        dispatch(userText(state));
        dispatch(botText(`How will you like to generate image for ${state}`));
        dispatch(setObjectName(state.toLowerCase()));
        dispatch(setStep(2));
        setState("");
      }
    } else if (stepStore.currentStep === 2) {
      if (state === generationProcessList[1]) {
        setDisableCheckBox(false);
        dispatch(userText(state));
        setDisableInput(true);
        getAllParts();
        dispatch(setStep(3));
      } else if (state === generationProcessList[0]) {
        dispatch(userText(state));
        getAllPartsForRandom();
        generateImageAPI([], "random");
        dispatch(setStep(3));
      }
      setState("");
    } else if (stepStore.currentStep === 3) {
      if (state === updateObjectList[2]) {
        dispatch(userText(state));
        dispatch(
          botText(`How will you like to generate image for ${objectName}`)
        );
        dispatch(setStep(2));
      } else if (state === updateObjectList[1]) {
        // Masked Image Update
        dispatch(userText(state));
        setDisableInput(true);
        setShowModal("masked");
      } else if (state === updateObjectList[0]) {
        // Masked Image Update
        dispatch(userText(state));
        setDisableInput(true);
        setShowModal("rectangle");
      } else if (state === updateObjectList[3]) {
        // Masked Image Update
        dispatch(userText(state));
        dispatch(setStep(1));
      }
      setState("");
    }
  };

  const updateAPI = (method) => {
    dispatch(addLoadingChat());
    setDisableInput(true);
    if (method === "masked") {
      axios
        .post(`${baseUrl}masked`, {
          data: { new_data: lines, old_data: serverStore.masked },
        })
        .then((response) => {
          console.log(response.data);
          dispatch(removeLoadingChat());
          dispatch(getImage(response.data.images));
          dispatch(setServerData(response.data));
          dispatch(setRectangles(response.data.rectangle));
          dispatch(setLines(response.data.masked));
          dispatch(botImage(response.data.images));
          dispatch(botText("What would you like to do next ?"));
          setDisableInput(false);
        });
    } else if (method === "rectangle") {
      axios
        .post(`${baseUrl}rectangle`, {
          data: { new_data: rectangles, old_data: serverStore.rectangle },
        })
        .then((response) => {
          console.log(response.data);
          dispatch(removeLoadingChat());
          dispatch(getImage(response.data.images));
          dispatch(setServerData(response.data));
          dispatch(setRectangles(response.data.rectangle));
          dispatch(setLines(response.data.masked));
          dispatch(botImage(response.data.images));
          dispatch(botText("What would you like to do next ?"));
          setDisableInput(false);
        });
    }
  };

  const handleIsDone = (modal) => {
    setDisableInput(false);
    setShowModal("");
    updateAPI(modal);
  };

  return (
    <div className={styles.container}>
      <div className={styles.chatContainer}>
        <div className={styles.messagesSection} ref={chatRef}>
          {chat.map((message) =>
            message.user === BOT ? (
              <div className={styles.leftMessage}>
                <div className={styles.bot}>B</div>
                <div className={styles.chat}>
                  {message.type === TEXT ? (
                    message.text
                  ) : message.type === IMAGE ? (
                    <div className={styles.imageContainer}>
                      <img
                        src={message.rect_image}
                        alt="reactangle image"
                        key={0}
                        className={styles.image}
                      />
                      <img
                        src={message.mask_image}
                        alt="masked image"
                        key={1}
                        className={styles.image}
                      />
                      <img
                        src={message.generated_image}
                        alt="generated image"
                        key={2}
                        className={styles.image}
                      />
                    </div>
                  ) : (
                    <form
                      className={styles.checkboxContainer}
                      onSubmit={handleSpecificPartsList}
                    >
                      <h3>{message.title}</h3>
                      <div className={styles.checkboxWrapper}>
                        {all_parts
                          ? all_parts.map((info) => (
                              <div>
                                <Checkbox
                                  color="primary"
                                  disabled={disableCheckBox}
                                  inputProps={{ name: info.part }}
                                />
                                <FormLabel>{info.full_part}</FormLabel>
                              </div>
                            ))
                          : null}
                      </div>
                      <div className={styles.buttonContainer}>
                        <Button
                          variant="contained"
                          color="primary"
                          type="submit"
                          className={styles.button}
                          disabled={disableCheckBox}
                        >
                          Done
                        </Button>
                      </div>
                    </form>
                  )}
                </div>
              </div>
            ) : message.user === USER ? (
              <div className={styles.rightMessage}>
                <div className={styles.chat}>{message.text}</div>
                <div className={styles.user}>U</div>
              </div>
            ) : message.user === INFO ? (
              <div className={styles.centerMessage}>
                <div className={styles.information}>{message.text}</div>
              </div>
            ) : (
              <div className={styles.leftMessage}>
                <div className={styles.bot}>B</div>
                <div className={styles.chat}>
                  <div className={styles.loader}>
                    <div className={styles.loader__circle}></div>
                    <div className={styles.loader__circle}></div>
                    <div className={styles.loader__circle}></div>
                    <div className={styles.loader__circle}></div>
                    <div className={styles.loader__circle}></div>
                  </div>
                </div>
              </div>
            )
          )}
        </div>
        <div className={styles.inputSection}>
          <form className={styles.inputSectionForm} onSubmit={handleSubmit}>
            <div className={styles.inputWrapper}>
              <Autocomplete
                value={state}
                id="combo-box-demo"
                options={
                  stepStore.currentStep === 1
                    ? objectsList
                    : stepStore.currentStep === 2
                    ? generationProcessList
                    : stepStore.currentStep === 3
                    ? updateObjectList
                    : []
                }
                getOptionLabel={(option) => option}
                autoHighlight
                onChange={(e, value) => setState(value)}
                clearOnEscape
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Enter Text"
                    id="outlined-basic"
                    fullWidth
                    variant="outlined"
                  />
                )}
                disabled={disableInput}
              />
            </div>
            <div className={styles.sendButtonContainer}>
              <Button
                variant="contained"
                color="primary"
                type="submit"
                className={styles.sendButton}
                disabled={disableInput}
                size="large"
              >
                Done
              </Button>
            </div>
          </form>
        </div>
      </div>
      {showModal === "masked" ? (
        <LineCanvasModal isDone={() => handleIsDone("masked")} />
      ) : showModal === "rectangle" ? (
        <RectangleCanvasModal isDone={() => handleIsDone("rectangle")} />
      ) : null}
    </div>
  );
}
