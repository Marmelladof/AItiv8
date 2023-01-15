import { createSlice } from "@reduxjs/toolkit";

export const form = createSlice({
  name: "form",
  initialState: {
    initialForm: false,
    savedCrop:[],
    savedPlanning:[],
  },
  reducers: {
    saveForm: (state) => {
      state.initialForm = true;
    },
    incrementByAmount: (state, action) => {
      state.value += action.payload;
    },
    addCrop: (state,action) => {
      state.savedCrop.push(action.payload);
    },
    addPlanning: (state, action) => {
      state.savedPlanning.push(action.payload);
    }
  },
});


// Action creators are generated for each case reducer function
export const { saveForm, incrementByAmount, addCrop, addPlanning } = form.actions;

export const state = (state) => state;

export default form.reducer;
