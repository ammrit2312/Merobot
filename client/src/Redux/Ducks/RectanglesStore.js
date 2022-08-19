const SET_RECTANGLES = 'set_rectangles';

const initState = {
    rect: []
};

export const setRectangles = (data) => {
    return{
        type: SET_RECTANGLES,
        data,
    }
}

export const RectanglesStore = (state = initState, action) => {
    switch (action.type){
        case SET_RECTANGLES:
            console.log(state)
            return{...state, rect: action.data};
        default:
            return state;
    }
};