import Form from "../form/Form";
import { useState, useEffect } from "react";
import { postCrop, postPlanning } from "../../api/apiList";
import {
  saveForm,
  saveFormPlanning,
  addPlanning,
  addCrop,
  addCropImage,
  addPlanningImage,
  state,
} from "../../redux/FormSlicer";
import { useSelector, useDispatch } from "react-redux";
import { useDebugValue } from "react";

function FormPage() {
  const [formData, setFormData] = useState([{ Space: "1" }]);
  const [planning, setPlanning] = useState();
  const [image, setImage] = useState();

  const dispatch = useDispatch();

  const cropSaved = useSelector(state).form.isCrop;
  const planningSaved = useSelector(state).form.isPlanning;
  const cropImage = useSelector(state).form.cropImage;
  const planningImage = useSelector(state).form.planningImage;

  function handleChange(formResult, planning, formId) {
    formData[formId] = formResult;
    setPlanning(planning);
    setFormData([...formData]);
  }

  const triggerSend = async () => {
    if (planning) {
      let response = await postPlanning(formData);
      dispatch(addPlanning(formData));
      dispatch(saveFormPlanning());
      dispatch(addPlanningImage(response));
    } else {
      let response = await postCrop(formData);
      dispatch(addCrop(formData));
      dispatch(saveForm());
      dispatch(addCropImage(response));
      setFormData([{ Interests: "1" }]);
      dispatch(addCropImage(response));
    }
  };

  if (cropSaved && !planningSaved) {
    return (
      <span>
        <h1 class=" mb-4 text-4xl font-extrabold  tracking-tight text-gray-800 md:text-5xl lg:text-1x1 text-white items-center justify-center max-w-4xl  mx-auto mt-5 ">
          Result{" "}
        </h1>
        <div class="flex text-white items-center justify-center max-w-4xl h-96 p-6 mx-auto bg-indigo-600 rounded-md shadow-md dark:bg-gray-800 mt-5 ">
          <figure class="allign-center max-w-lg">
            <img
              class="h-auto max-w-full rounded-lg"
              src={`data:image/png;base64,${cropImage}`}
              alt="Recommended Crop Distribuition"
            />
            <figcaption class="mt-2 text-sm text-center text-gray-500 dark:text-gray-400">
              Recommended Crop Distribution
            </figcaption>
          </figure>
        </div>
        <div>
          <Form
            formId={0}
            onFormChange={(formResult, planning, formId) =>
              handleChange(formResult, planning, formId)
            }
          />
          {/* <p>{JSON.stringify(item)}</p> */}
        </div>
        <div class="mb-10 left-1/4 w-1/2 grid grid-cols-4 gap-20 relative mt-10">
          <button
            class="right-7 absolute px-6 py-2 leading-5 text-white transition-colors duration-200 transform bg-pink-500 rounded-md hover:bg-pink-700  "
            onClick={() => triggerSend()}
          >
            Send
          </button>
        </div>
      </span>
    );
  } else if (planningSaved) {
    return (
      <span>
        <h1 class=" mb-4 text-4xl font-extrabold  tracking-tight text-gray-800 md:text-5xl lg:text-1x1 text-white items-center justify-center max-w-4xl  mx-auto mt-5 ">
          Result{" "}
        </h1>
        <div class="flex text-white items-center justify-center max-w-4xl mb-5 p-6 mx-auto bg-indigo-600 rounded-md shadow-md dark:bg-gray-800 mt-5 ">
          <figure class="max-w-lg">
            <img
              class="h-auto max-w-full rounded-lg"
              src={`data:image/png;base64,${planningImage}`}
              alt="Recommended Crop Distribuition With Added Interests"
            />
            <figcaption class="mt-2 text-sm text-center text-gray-500 dark:text-gray-400">
              Recommended Crop Distribution With Added Interests
            </figcaption>
          </figure>
        </div>
      </span>
    );
  } else {
    return (
      <span>
        {formData.map((item, index) => (
          <div>
            <Form
              formId={index}
              onFormChange={(formResult, planning, formId) =>
                handleChange(formResult, planning, formId)
              }
            />
            {/* <p>{JSON.stringify(item)}</p> */}
          </div>
        ))}
        <div class="mb-10 left-1/4 w-1/2 grid grid-cols-4 gap-20 relative mt-10">
          <button
            class="px-6 py-2 left-7 absolute leading-5 text-white transition-colors duration-200 transform bg-pink-500 rounded-md hover:bg-pink-700 focus:outline-none "
            onClick={() => {
              let Space = formData.length;
              formData.push({ Space });
              setFormData([...formData]);
            }}
            disabled={cropSaved}
          >
            Add Form
          </button>
          <button
            class="right-7 absolute px-6 py-2 leading-5 text-white transition-colors duration-200 transform bg-pink-500 rounded-md hover:bg-pink-700  "
            onClick={() => triggerSend()}
          >
            Send
          </button>
        </div>
      </span>
    );
  }
}

export default FormPage;
