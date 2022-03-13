import "./App.css";
import ImageUploader from "./components/ImageUploader";
import Navbar from "./components/Navbar";
import toast, { Toaster } from "react-hot-toast";

function App() {
  return (
    <div>
      <div>
        <Toaster />
      </div>
      <Navbar />
      <div className="topMargin"></div>
      <ImageUploader />
    </div>
  );
}

export default App;
