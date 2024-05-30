  import React, { useEffect, useState } from "react";
  import "./App.css";
  import foodData from "./data/Fooddata.json";
  import FoodItem from "./components/FoodItem";
  import Instructions from "./components/Instructions";
  import Ingredients from "./components/Ingredients";
  import Footer from "./components/Footer";
  import ImageUpload from "./components/ImageUpload";

  function App() {
    const [data, setData] = useState({ class: "Default", confidence: 100 });
    const [food, setFood] = useState(foodData["Default"]);
    const [err, setErr] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");

    useEffect(() => {
      setFood(foodData[data.class]);
    }, [data]);

    // Function to handle search input change
  const handleSearchInputChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSearch = () => {
    let sanitizedQuery = searchQuery.trim().toLowerCase();
    sanitizedQuery = sanitizedQuery.charAt(0).toUpperCase() + sanitizedQuery.slice(1);

    // Check if the searched item exists in the dataset
    if (foodData[sanitizedQuery]) {
      setData({ class: sanitizedQuery, confidence: "100" });
      setErr(false); // Reset error state if the item is found
    } else {
      setErr(true); // Set error state if the item is not found
    }
  };
  

    return (
      <div className="App">
        <nav className="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            <img src="/assets/favicon.ico" alt="logo" className="pe-3" />
            SnapNPlate
          </a>
          <div className="d-flex align-items-center">
            <input
              type="text"
              className="form-control me-2"
              placeholder="Search..."
              value={searchQuery}
              onChange={handleSearchInputChange}
            />
            <button className="btn btn-outline-light" onClick={handleSearch}>
              Search
            </button>
          </div>
        </div>
      </nav>
        {err && (
          <div class="alert alert-secondary" role="alert">
            We couldn't confidently classify the provided image based on our
            current dataset. Please ensure the photo is clear and well-lit, or try
            another angle for a more accurate classification. If the issue
            persists, it may be a unique or uncommon food item not currently in
            our database. Thank you for your understanding.
          </div>
        )}
        <div className="row">
          <FoodItem
            name={data.class}
            description={food["description"]}
            nutrientFacts={food["nutrientfact"]}
            veg={food["veg"]}
            prepTime={food["preptime"]}
            cookingTime={food["cookingtime"]}
            serving={food["serving"]}
          />
        </div>
        <div className="row">
          <ImageUpload setData={setData} setErr={setErr} />
        </div>
        <div className="row">
          <div className="col-12 col-xl-6">
            <Instructions instructions={food["instruction"]} />
          </div>
          <div className="col-12 col-xl-6">
            <Ingredients ingredients={food["ingredients"]} />
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  export default App;
