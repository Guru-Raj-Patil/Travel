import React from "react";
import "./app.css";
import Navbar from "./Components/Navbar/Navbar";
import Home from "./Components/Home/Home";
import Main from "./Components/Main/Main"; // Add import statement for Main component
import Footer from "./Components/Footer/Footer"; // Add import statement for Footer component
import DestinationDetails from "./Components/Main/DestinationDetails";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Navbar />
              <Home />
              <Main />
              <Footer />
            </>
          }
        />
        <Route
          path="/destination/:destTitle"
          element={<DestinationDetails />}
        />
      </Routes>
    </Router>
  );
};

export default App;
