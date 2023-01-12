import { createSlice } from "@reduxjs/toolkit";

export const FormSlicer = createSlice({
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
export const { saveForm, incrementByAmount } = FormSlicer.actions;

export const state = (state) => state;

export default FormSlicer.reducer;
