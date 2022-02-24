import "./App.css";
import ImageUploader from "./components/ImageUploader";
import Navbar from "./components/Navbar";

const fileTypes = ["JPG", "PNG", "GIF", "JPEG"];

function App() {
  return (
    <div className="stuff">
      <Navbar />
      <ImageUploader />
    </div>
  )
}

export default App;
