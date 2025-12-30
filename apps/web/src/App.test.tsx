import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "./App";

import "@testing-library/jest-dom";

describe("App", () => {
  it("renders heading", () => {
    render(<App />);
    expect(screen.getByText(/SLSA Nexus/)).toBeInTheDocument();
  });
});
