const initialState = { currentStep: 1 };

// STEPS -

// Step 1: Select Object
// Call API for getting the list of all_parts

// Step 2: Select Property (Random / Specific)

// Step 3: Continue Editing the Object
// If Yes then Step 4
// Else Regerate Image.

// Step 3: Select Which Image to Change
// Back to Step 2

export const setStep = (step) => {
  return {
    type: "SET_STEP",
    step,
  };
};

export const StepStore = (state = initialState, action) => {
  switch (action.type) {
    case "SET_STEP":
      return {
        ...state,
        currentStep: action.step,
      };
    default:
      return state;
  }
};
