import React from "react";
import styles from "./Navbar.module.css";
import { useHistory } from "react-router-dom";
import logo from "../../Assets/logo-2.png";
import logo1 from "../../Assets/logo-1.jpg";

export default function Navbar() {
  const history = useHistory();
  return (
    <div className={styles.Container}>
      <div className={styles.logo} onClick={() => history.push("/")}>
        Merobot
      </div>
      <div className={styles.linksContainer}>
        <img src={logo} className={styles.CollegeLogo} />
        <img src={logo1} className={styles.CollegeLogo} />
      </div>
    </div>
  );
}
