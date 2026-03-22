"use client";

import { useState } from "react";
import { search24 } from "@esri/calcite-ui-icons";

export default function SearchPanel() {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    console.log("Searching for:", query);
  };

  return (
    <div className="m-5 flex w-[30vw] items-center overflow-hidden rounded-md bg-white text-black shadow-md">
      <input
        type="text"
        placeholder="Search by Parcel ID"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-1 px-5 py-2 outline-none"
      />

      <button
        onClick={handleSearch}
        className="flex cursor-pointer items-center justify-center bg-blue-500 px-3 py-2 text-black hover:bg-blue-600"
      >
        <svg className="h-6 w-6" viewBox="0 0 24 24" fill="currentColor">
          <path d={search24} />
        </svg>
      </button>
    </div>
  );
}
