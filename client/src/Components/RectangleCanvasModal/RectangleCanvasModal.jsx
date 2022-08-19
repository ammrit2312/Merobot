import React, { useState } from "react";
import styles from "./RectangleCanvasModal.module.css";
import Canvas, { RECTANGLE } from "../Canvas/Canvas.js";
import { useSelector } from "react-redux";
import {BiRectangle, BiEraser} from "react-icons/bi"


export default function RectangleCanvasModal(props) {
  const rectangles = useSelector((state) => state.Rectangles.rect);
  const imageStore = useSelector((state) => state.ImageStore);
  const remainingPartsList = useSelector(
    (state) => state.ServerStore.remaining_parts
  );


  const [color, setColor] = useState("#000000");
  const [selection, setSelection] = useState('rectangle');
  return (
    <div className={styles.container}>
      <div className={styles.imgContainer}>
        <img src={imageStore.mask_image} alt="img" className={styles.image} />
        <img
          src={imageStore.generated_image}
          alt="img"
          className={styles.image}
        />
      </div>
      <Canvas tool={RECTANGLE} selection={selection} color={color} />
      <div className={styles.sideBar}>
        <div>
          <div className={styles.input}>
            <BiRectangle
              onClick={(e) => setSelection("rectangle")}
              className={styles.optionIcons}
            />
            <BiEraser
              onClick={(e) => setSelection("eraser")}
              className={styles.optionIcons}
            />
          </div>
          {/* <label for="colorPicker">Stroke Colour : </label>
          <input
            type="color"
            value={color}
            id="colorPicker"
            onChange={(e) => setColor(e.target.value)}
          /> */}
          <div>
            <h4>List of existing parts</h4>
            <table className={styles.Table}>
              <tr>
                <th>Part</th>
                <th>Color</th>
              </tr>
              {rectangles.map((line, index) => (
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
              {remainingPartsList.map((part, index) => (
                <li key={index}>{part.full_part}</li>
              ))}
            </ul>
          </div>
          <div className={styles.Button} onClick={() => props.isDone(process)}>Done</div>
        </div>
      </div>
    </div>
  );
}
