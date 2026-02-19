# External libraries
import pickle
import math
import matplotlib.pyplot as plt
import numpy as np
            
# Utility for loading saved data
class DataLoader:

    # Constructor
    def __init__(self, filename):
        self.filename = filename
        
    # Load a dictionary from file.
    def load(self):
        with open(self.filename, 'rb') as file_handle:
            loaded_dict = pickle.load(file_handle)
        return loaded_dict
        
def plot_leg_path(data_dictionary):
    time_stamp_list = data_dictionary['time_stamp']
    theta1_f_list = data_dictionary['theta1_f']
    theta2_f_list = data_dictionary['theta2_f']
    theta3_f_list = data_dictionary['theta3_f']
    theta1_b_list = data_dictionary['theta1_b']
    theta2_b_list = data_dictionary['theta2_b']
    theta3_b_list = data_dictionary['theta3_b']
    end_effector_position_f = np.array(data_dictionary['end_effector_position_f'])
    end_effector_position_b = data_dictionary['end_effector_position_b']
    x_ee_f =end_effector_position_f[:,0]
    y_ee_f =end_effector_position_f[:,1]
    z_ee_f =end_effector_position_f[:,2]


    plt.figure(figsize=(8,5))
    plt.plot(x_ee_f, y_ee_f)
    plt.title('End Effector trajectory')
    plt.xlabel('EE X(m)')
    plt.ylabel('EE Y(m)')
    plt.ylim(0, 0.20)
    #plt.show()
    plt.savefig("2_ee_xy_trajectory.png")
    plt.close()

    # plt.figure(figsize=(8,5))
    # plt.plot(time_stamp_list, x_ee_f)
    # plt.title('End Effector trajectory')
    # plt.xlabel('Time(s)')
    # plt.ylabel('EE X(m)')
    # #plt.show()
    # plt.savefig("2_ee_xt_trajectory.png")
    # plt.close()

    # plt.figure(figsize=(8,5))
    # plt.plot(time_stamp_list,z_ee_f )
    # plt.title('End Effector Z vs Time')
    # plt.xlabel('Time(s)')
    # plt.ylabel('EE Z (m)')
    # plt.ylim(0, -0.2)
    # #plt.show()
    # plt.savefig("2_ee_zt_trajectory.png")
    # plt.close()



##### MAIN ######

data_loader = DataLoader('/home/pi/team_say/NYU_ROB_UY_2004/Labs/Lab2/NYU_ROB_UY_2004/Labs/Lab2/lab_2_data.pkl')
data_dictionary = data_loader.load()
plot_leg_path(data_dictionary)
