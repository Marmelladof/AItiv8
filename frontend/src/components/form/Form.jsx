import { useForm } from "react-hook-form";
import { useState } from "react";
import { postCrop } from "../../api/apiList";
import { state, saveForm } from "../../redux/FormSlicer";
import { useSelector, useDispatch } from "react-redux";

const dados = [
  { label: "area", type: "number" },
  {
    label: "N",
    type: "number",
  },
  {
    label: "P",
    type: "number",
  },
  {
    label: "K",
    type: "number",
  },
  {
    label: "temperature",
    type: "number",
  },
  {
    label: "humidity",
    type: "number",
  },
  {
    label: "ph",
    type: "number",
  },
  {
    label: "rainfall",
    type: "number",
  },
];
const dadosPlan = [
  { label: "trocu", type: "number" },
  {
    label: "321",
    type: "number",
  },
  {
    label: "dsadas a",
    type: "number",
  },
];

function Form(props) {
  const { register, handleSubmit } = useForm();

  const [disabled, setDisabled] = useState(false);
  const [editSend, setEditSend] = useState("Save");

  const formState = useSelector(state).form.initialForm;
  const dispatch = useDispatch();
  return (
    <div>
      <section class="max-w-4xl p-6 mx-auto bg-indigo-600 rounded-md shadow-md dark:bg-gray-800 mt-20">
        <button onClick={() => dispatch(saveForm())}>Alterar state</button>
        <h1 class="text-xl font-bold text-white capitalize dark:text-white">
          Campo {props.formId}
        </h1>
        <form
          class="relative"
          onSubmit={handleSubmit((data) => formSaveHandler(data))}
        >
          <div class="grid grid-cols-1 gap-5 mt-4 sm:grid-cols-3">
            {formState
              ? dadosPlan.map((dado, i) => (
                  <div>
                    <label
                      style={{ textTransform: "capitalize" }}
                      class="text-white dark:text-gray-200"
                      for={dado.label}
                    >
                      {dado.label}
                    </label>
                    <input
                      {...register(dado.label, {
                        required: true,
                        disabled: disabled,
                      })}
                      id={dado.label}
                      type={dado.type}
                      step={0.00000000000001}
                      class="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring"
                    />
                  </div>
                ))
              : dados.map((dado, i) => (
                  <div>
                    <label
                      style={{ textTransform: "capitalize" }}
                      class="text-white dark:text-gray-200"
                      for={dado.label}
                    >
                      {dado.label}
                    </label>
                    <input
                      {...register(dado.label, {
                        required: true,
                        disabled: disabled,
                      })}
                      id={dado.label}
                      type={dado.type}
                      step={0.00000000000001}
                      class="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-500 dark:focus:border-blue-500 focus:outline-none focus:ring"
                    />
                  </div>
                ))}
          </div>
          <button
            class="px-6 absolute bottom-5 right-0 py-2 leading-5 text-white transition-colors duration-200 transform bg-pink-500 rounded-md hover:bg-pink-700 focus:outline-none focus:bg-gray-600"
            type="submit"
          >
            {editSend}
          </button>
          <div class="flex justify-end mt-6" />
        </form>
      </section>
    </div>
  );

  function formSaveHandler(Parameters) {
    if (!disabled) {
      props.onFormChange(Parameters, formState, props.formId);
    }
    disabled ? setDisabled(false) : setDisabled(true);
    disabled ? setEditSend("Save") : setEditSend("Edit");
  }
}

export default Form;
