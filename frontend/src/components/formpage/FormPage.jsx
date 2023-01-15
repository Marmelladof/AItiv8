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

  const base64 =
    "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";

  function handleChange(formResult, planning, formId) {
    formData[formId] = formResult;
    setPlanning(planning);
    setFormData([...formData]);
  }

  const triggerSend = async () => {
    console.log(formData);
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
        <figure class="max-w-lg">
          <img
            class="h-auto max-w-full rounded-lg"
            src={`data:image/png;base64,${cropImage}`}
            alt="Recommended Crop Distribuition"
          />
          <figcaption class="mt-2 text-sm text-center text-gray-500 dark:text-gray-400">
            Recommended Crop Distribution
          </figcaption>
        </figure>
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
        <figure class="max-w-lg">
          <img
            class="h-auto max-w-full rounded-lg"
            src={`data:image/png;base64,${cropImage}`}
            alt="Recommended Crop Distribuition"
          />
          <figcaption class="mt-2 text-sm text-center text-gray-500 dark:text-gray-400">
            Recommended Crop Distribution
          </figcaption>
        </figure>

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
