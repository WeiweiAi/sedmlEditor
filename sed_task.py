from sedDict import create_dict_sedDocment, add_sedTask2dict
from sedEditor import create_sedDocment,write_sedml, validate_sedml, read_sedml

def sedtask():

    # Convert the model to CellML 2.0 if needed
    path_='./models/'
    model_name='SGLT1_BG_step_ss'

    model_ids_=['_fig5_m150mV','_fig5_m120mV','_fig5_m80mV','_fig5_m50mV','_fig5_m30mV','_fig5_0mV','_fig5_40mV','_fig5_50mV','_fig5_80mV',
                '_fig5_m150mV_sugar','_fig5_m120mV_sugar','_fig5_m80mV_sugar','_fig5_m50mV_sugar','_fig5_m30mV_sugar','_fig5_0mV_sugar',
                '_fig5_40mV_sugar','_fig5_50mV_sugar','_fig5_80mV_sugar',]
    test_volts=['-0.15','-0.12','-0.08','-0.05','-0.03','0','0.04','0.05','0.08',
                '-0.15','-0.12','-0.08','-0.05','-0.03','0','0.04','0.05','0.08',]
    Glcos=['1e-12','1e-12','1e-12','1e-12','1e-12','1e-12','1e-12','1e-12','1e-12','1','1','1','1','1','1','1','1','1']
    dict_sedDocument=create_dict_sedDocment()
    # This is the sedml file (relative) path and name, assuming in the same folder with the CellML model file
    sedpath_=path_
    sedFilename = model_name+'.sedml' 
    full_path = sedpath_+ sedFilename 

    for i in range(len(model_ids_)):
        model_id_=model_ids_[i]
        test_volt=test_volts[i]
        Glco=Glcos[i]
        # ********** The following is to create a dictionary for the sedml file **********
       
        
        # model_name='Boron_acid_EA'
        model_id = model_name+model_id_ # This is the model id in the sedml, could be different from the model file name        

        # ********** The following is to add the task information to the dictionary **********

        # Note: the following is an example, you can modify it to add more tasks
        # Note: the valid sedml id should start with a letter, and only contain letters, numbers, and underscores
        # This is the model file name, assuming in the same folder with the sedml file
        model_source = model_name + '.cellml' 
        # This is to modify the model parameters if needed
        changes={'test_volt':{'component':'params_BG','name':'test_volt','newValue':test_volt},
                 'Glco':{'component':'params_BG','name':'Glco','newValue':Glco}
                 } 
        # the format is {'id':{'component':str,'name':str,'newValue':str}}
        # Example: changes={'V_m':{'component':'main','name':'V_m','newValue':'-0.055'}

        # This is the output of the simulation, and the key is part of the output id
        # The value is a dictionary with the following keys: 'component', 'name', 'scale'
        # component is the component name in the CellML model where the output variable is defined
        # name is the variable name of the outputs
        # scale is the scaling factor for the output variable
        outputs={'t':{'component':'SGLT1_BG','name':'t','scale':1},
                 'Ii':{'component':'SGLT1_BG','name':'Ii','scale':-1e-6},         
                 'I_ss':{'component':'SGLT1_BG','name':'I_ss','scale':1e-6},
                 'V0_Vm':{'component':'params_BG','name':'V0_Vm','scale':1e3},
                 'V_E':{'component':'params_BG','name':'V_E','scale':1e3},
                 }
        # You can add more outputs if needed

        # The following is the simulation setting
        # This is to set the maximum step size for the simulation
        dict_algorithmParameter={'kisaoID':'KISAO:0000209', 'name':'rtol','value':'1e-12'} 
        dict_algorithmParameter2={'kisaoID':'KISAO:0000211', 'name':'atol','value':'1e-12'} 
        # You can set more algorithm parameters if needed. You can refer to get_KISAO_parameters() in src/simulator.py file to get the parameters for the specific algorithm
        # Add the algorithm parameters to listOfAlgorithmParameters
        # You can choose one of the simulation algorithms specified by KISAO_ALGORITHMS in src/simulator.py file
        dict_algorithm={'kisaoID':'KISAO:0000535','name':'VODE','listOfAlgorithmParameters':[dict_algorithmParameter,dict_algorithmParameter2]} 
        # This is the simulation setting
        # You can choose one of the following simulation types: 'UniformTimeCourse', 'OneStep'
        simSetting={'type':'UniformTimeCourse','algorithm':dict_algorithm,'initialTime':0,'outputStartTime':0,'outputEndTime':3,'numberOfSteps':30000}
        # simSetting={'type':'OneStep','algorithm':dict_algorithm,'step':0.1}


        # The following is to add the task information to the dictionary
        add_sedTask2dict(dict_sedDocument, model_id, model_source,changes,simSetting,outputs)

        # You can repeat the above steps to add more tasks with DIFFERENT model names.

    # ********** The following is to create the sedml file, no need to modify **********
    try:
        doc=create_sedDocment(dict_sedDocument)
    except ValueError as err:
        print(err)
    write_sedml(doc,full_path)
    print(validate_sedml(full_path))
    doc=read_sedml(full_path) # Must read the sedml file again to avoid the error in the next step

sedtask()