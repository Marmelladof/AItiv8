import { configureStore } from "@reduxjs/toolkit";
import FormSlicer from "./redux/FormSlicer";

export default configureStore({
  reducer: {
    form: FormSlicer,
  },
});
