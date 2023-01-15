import { createSlice } from "@reduxjs/toolkit";

export const form = createSlice({
  name: "form",
  initialState: {
    isCrop: false,
    isPlanning: false,
    savedCrop: [],
    savedPlanning: [],
    cropImage: "",
    planningImage: "",
  },
  reducers: {
    saveFormPlanning: (state) => {
      state.isPlanning = true;
    },
    saveForm: (state) => {
      state.isCrop = true;
    },
    addCrop: (state, action) => {
      state.savedCrop.push(action.payload);
    },
    addPlanning: (state, action) => {
      state.savedPlanning.push(action.payload);
    },
    addCropImage: (state, action) => {
      state.cropImage = action.payload;
    },
    addPlanningImage: (state, action) => {
      state.planningImage = action.payload;
    },
  },
});

// Action creators are generated for each case reducer function
export const {
  saveForm,
  saveFormPlanning,
  addCropImage,
  addCrop,
  addPlanning,
  addPlanningImage,
} = form.actions;

export const state = (state) => state;

export default form.reducer;
