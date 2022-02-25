import "./App.css";
import ImageUploader from "./components/ImageUploader";
import Navbar from "./components/Navbar";

function App() {
  return (
    <div>
      <Navbar />
      <div className="topMargin"></div>
      <ImageUploader />
    </div>
  )
}

export default App;
