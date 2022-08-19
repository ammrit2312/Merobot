import React, { useRef } from "react";
import { Line } from "react-konva";

const LineComponent = (props) => {
  const shapeRef = useRef();

  return (
    <React.Fragment>
      <Line
        key={props.keyValue}
        points={props.points}
        stroke={props.stroke}
        closed={props.closed}
        fill={props.fill}
        strokeWidth={props.strokeWidth}
        draggable={false}
        onClick={props.onSelect}
        onTap={props.onSelect}
        ref={shapeRef}
        onDragStart={(e) => props.onDragStart(e, props.keyValue)}
      />
    </React.Fragment>
  );
};

export default LineComponent;