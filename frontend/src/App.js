import "./App.css";
import Home from "./components/home/Home";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/navbar/Navbar";
import FormPage from "./components/formpage/FormPage";


function App() {
  return (
    <Router>
      <Navbar></Navbar>
      <Routes>
        <Route path="/" element={<FormPage/>}></Route>
        <Route path="/form" element={<FormPage/>}></Route>
      </Routes>
    </Router>
  );
}

export default App;
