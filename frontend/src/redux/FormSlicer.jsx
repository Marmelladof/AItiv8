import { createSlice } from "@reduxjs/toolkit";

export const form = createSlice({
  name: "form",
  initialState: {
    initialForm: false,
  },
  reducers: {
    saveForm: (state) => {
      state.initialForm = true;
    },
    incrementByAmount: (state, action) => {
      state.value += action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const { saveForm, incrementByAmount } = form.actions;

export const state = (state) => state;

export default form.reducer;
