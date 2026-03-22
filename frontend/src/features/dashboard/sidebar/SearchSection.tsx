"use client";

import { useState } from "react";
import { search24 } from "@esri/calcite-ui-icons";

export default function SearchPanel() {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    console.log("Searching for:", query);
  };

  return (
    <div className="m-5 flex items-center w-[30vw] bg-white shadow-md rounded-md overflow-hidden text-black">
      <input
        type="text"
        placeholder="Search by Parcel ID"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-1 px-5 py-2 outline-none"
      />

      <button
        onClick={handleSearch}
        className="bg-blue-500 hover:bg-blue-600 text-black px-3 py-2 flex items-center justify-center cursor-pointer"
      >
        <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
          <path d={search24} />
        </svg>
      </button>
    </div>
  );
}
