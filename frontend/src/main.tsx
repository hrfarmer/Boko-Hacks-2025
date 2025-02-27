import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import Navbar from "./components/Navbar";
import "./index.css";
import AdminPortal from "./routes/Admin";
import Home from "./routes/Home";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Navbar />}>
          <Route path="/" element={<Home />} />
          <Route path="/admin" element={<AdminPortal />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
