function [outLayers, allRoughs] = callParaMatalbCustlay(problemDef,problemDef_cells,...
    problemDef_limits,controls)


% Extract individual cell arrays
[repeatLayers,...
 allData,...
 dataLimits,...
 simLimits,...
 contrastLayers,...
 layersDetails...
 customFiles] = RAT_parse_cells(problemDef_cells);

% Extract individual parameters from problemDef struct
[numberOfContrasts, geometry, cBacks, cShifts, cScales, cNbas, cNbss,...
cRes, backs, shifts, sf, nba, nbs, res, dataPresent, nParams, params,...
numberOfLayers, resample, backsType, cCustFiles] =  extractProblemParams(problemDef);

% Call the loop custom....
% We feval into the Matlab base workspace here, and allow the paralell computing toolbox (if
% present) to loop over the function calls.
[tempOutLayers, tempAllRoughs] = feval('loopMatlabCustomLayers',cBacks,cShifts,cScales,cNbas,cNbss,cRes,backs,...
    shifts,sf,nba,nbs,res,cCustFiles,numberOfContrasts,customFiles,params);

% May need some recasting here?
outLayers = tempOutLayers;
allRoughs = tempAllRoughs;

end


