import React from "react";
import Navbar from "./Components/Navbar/Navbar";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import MainPage from "./Components/MainPage/MainPage";
import LineCanvasModal from "./Components/LineCanvasModal/LineCanvasModal";

function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route exact path="/" component={MainPage} />
        {/* <Route exact path="/product" component={Product} />
        <Route exact path="/about" component={About} /> */}
        {/* <Route exact path="/try" component={LineCanvasModal} /> */}
      </Switch>
    </Router>
  );
}

export default App;
