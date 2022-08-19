import React, { useState } from "react";
import styles from "./LineCanvasModal.module.css";
import Canvas, { LINE } from "../Canvas/Canvas.js";
import { useSelector } from "react-redux";
import { BsPencil } from "react-icons/bs";
import { BiEraser } from "react-icons/bi";

export default function LineCanvasModal(props) {
  const lines = useSelector((state) => state.Lines.line);
  const imageStore = useSelector((state) => state.ImageStore);
  const remainingPartsList = useSelector(
    (state) => state.ServerStore.remaining_parts
  );

  // const [color, setColor] = useState("#000000");
  const color = "#000000";
  const [fillColor, setFillColor] = useState("#FeB142");

  //delete
  const [selection, setSelection] = useState("pencil");
  return (
    <div className={styles.container}>
      <div className={styles.imgContainer}>
        <img src={imageStore.rect_image} alt="img" className={styles.image} />
        <img
          src={imageStore.generated_image}
          alt="img"
          className={styles.image}
        />
      </div>
      <Canvas
        tool={LINE}
        selection={selection}
        color={color}
        fillColor={fillColor}
      />
      <div className={styles.sideBar}>
        <div>
          <div className={styles.input}>
            {/* <select
              value = {selection}
              onChange = {e=>setSelection(e.target.value)}
            >
              <option value = "pencil">Pencil</option>
              <option value = "eraser">Eraser</option>
            </select> */}
            <BsPencil
              onClick={(e) => setSelection("pencil")}
              className={styles.optionIcons}
            />
            <BiEraser
              onClick={(e) => setSelection("eraser")}
              className={styles.optionIcons}
            />
          </div>
          <div>
            <h4>List of existing parts</h4>
            <table className={styles.Table}>
              <tr>
                <th>Part</th>
                <th>Color</th>
              </tr>
              {lines.map((line, index) => (
                <tr key={index}>
                  <td>{line.label}</td>
                  <td
                    className={styles.Td}
                    style={{ backgroundColor: line.stroke }}
                  ></td>
                </tr>
              ))}
            </table>
            {/* {lines.map((line, index) => (
              <div className={styles.labelsUsed}>
                <p>{line.label}</p>
                <div
                  className={styles.Td}
                  style={{ backgroundColor: line.stroke }}
                ></div>
              </div>
            ))} */}
          </div>
          <div>
            <h4>List of remaining parts</h4>
            {/* <table className={styles.Table}>
              <tr>
                <th>Part</th>
              </tr>
              {remainingPartsList.map((part, index) => (
                <tr key={index}>
                  <td className={styles.remaining}>{part.full_part}</td>
                </tr>
              ))}
            </table> */}
            <ul className={styles.remaining}>
              {remainingPartsList.length ? remainingPartsList.map((part, index) => (
                <li key={index}>{part.full_part}</li>
              )): <p>No parts remaining</p>}
            </ul>
          </div>
          <div className={styles.Button} onClick={props.isDone}>
            Done
          </div>
        </div>
      </div>
    </div>
  );
}
