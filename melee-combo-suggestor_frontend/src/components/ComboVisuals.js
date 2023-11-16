import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const ComboVisuals = ({ data }) => {
    const d3Container = useRef(null);

    useEffect(() => {
        if (data && d3Container.current) {
        }
    }, [data]);

    return (
        <div ref={d3Container}></div> 
    );
};

export default ComboVisuals;
