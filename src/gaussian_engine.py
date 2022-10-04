import os,sys, subprocess
import multiprocessing


from ase.io import read
from ase.calculators.gaussian import Gaussian, GaussianOptimizer


def gaussian_engine(xyz_file, var, output_dir):
    ## Geometry Optimization ##
    if var.geom_opt == True:
        if os.path.isdir('geom_opt') == False:
            os.mkdir('geom_opt')
            os.chdir('geom_opt')
        else:
            os.chdir('geom_opt')

        subprocess.call([f'cp {output_dir}/file_prep/'+xyz_file+' .'], shell=True)

        # If Geometry Converged Skip otherwise Run Again#
        if os.path.exists(f'{output_dir}/QM/geom_opt/geom_opt.chk') == False:
            gaussian_geom_opt(xyz_file, var)
            gaussian_opt_converged('geom_opt.log')
        
        if gaussian_opt_converged('geom_opt.log') == True:
            pass

        extract_xyz(xyz_file)

        ## Single Point ##
        os.chdir(f'{output_dir}/QM')

        if os.path.isdir('single_point') == False:
            os.mkdir('single_point')
            os.chdir('single_point')
        else:
            os.chdir('single_point')

        subprocess.call([f'cp {output_dir}/QM/geom_opt/output.xyz .'], shell=True)

        if os.path.exists(f'{output_dir}/QM/single_point/single_point.chk') == False:
            gaussian_sp('output.xyz', var)
            extract_CM5('single_point.log', 'output.xyz')
            subprocess.call(["grep  'SCF Done' single_point.log > energy"], shell=True)
        
        if gaussian_sp_converged('single_point.log') == True:
            extract_CM5('single_point.log', 'output.xyz')
            subprocess.call(["grep  'SCF Done' single_point.log > energy"], shell=True)
        
    else:
        ## Single Point ##
        os.chdir(f'{output_dir}/QM')

        if os.path.isdir('single_point') == False:
            os.mkdir('single_point')
            os.chdir('single_point')
        else:
            os.chdir('single_point')

        subprocess.call([f'cp {output_dir}/file_prep/'+xyz_file+' output.xyz'], shell=True)
        
        if os.path.exists(f'{output_dir}/QM/single_point/single_point.chk') == False:
            gaussian_sp('output.xyz', var)
            gaussian_sp_converged('single_point.log')
            extract_CM5('single_point.log', 'output.xyz')
            subprocess.call(["grep  'SCF Done' single_point.log > energy"], shell=True)
        
        if gaussian_sp_converged('single_point.log') == True:
            extract_CM5('single_point.log', 'output.xyz')
            subprocess.call(["grep  'SCF Done' single_point.log > energy"], shell=True)

    return os.getcwd()        

    
def extract_CM5(log_file, xyz_file):
    mol = read(xyz_file)
    N = len(mol.positions) 

    subprocess.call(["grep -A"+str(N+1)+" 'Hirshfeld charges, spin densities, dipoles, and CM5 charges' "+log_file+" > charge_1"], shell=True)
    with open('charge_1','r') as fin:
        with open('CM5_charges','w') as fout:
            fin_lines = [line.split() for line in fin]

            for i in fin_lines[2:]:
                fout.write('{} {}\n'.format(i[1],i[6]))

    subprocess.call(['rm charge_1'], shell=True)
    return

            
def gaussian_opt_converged(log_file):
     with open(log_file) as log:
        if 'Optimization completed.' in log.read():
            print('GEOMETRY CONVERGED')
            return True
        else:
            print('GEOMETRY NOT CONVERGED - DELETE .chk AND RERUN')
            return sys.exit()


def gaussian_geom_opt(xyz_file, var):
    n_procs = 32 #multiprocessing.cpu_count()
    M = 2 * var.spin + 1 

    mol = read(xyz_file)
    symbols = list(mol.symbols)

    s   = Gaussian(label='geom_opt',
                    nprocshared=n_procs,
                    mem='4GB',
                    chk='geom_opt.chk',
                    xc=var.functional,
                    charge=var.charge,
                    mult=M,
                    basis=var.basis_set,
                    pop='Hirshfeld',
                    SCRF='Solvent=Water',
                    EmpiricalDispersion=var.dispersion)

    opt = GaussianOptimizer(mol, s)
    opt.run(fmax='tight')

    return 
        
def extract_xyz(xyz_file):
    mol = read(xyz_file)
    symbols = list(mol.symbols)
    N = len(mol.positions) 

    subprocess.call(["grep -A10000 'Optimization completed' geom_opt.log > file_1"], shell=True)
    subprocess.call(["grep -A"+str(N+4)+" 'Input orientation' file_1 > file_2"], shell=True)

    with open('file_2','r') as fin:
        with open('output.xyz','w') as fout:
            fin_lines = [line.split() for line in fin]

            fout.write('{}\n\n'.format(len(mol.positions)))
            for idx, i in enumerate(fin_lines[5:]):
                fout.write('{} {} {} {}\n'.format(symbols[idx],i[3], i[4], i[5]))

    subprocess.call(['rm file_1 file_2'], shell=True)

    return N

def gaussian_sp(xyz_file, var):
    n_procs = multiprocessing.cpu_count()
    M = 2 * var.spin + 1 

    metal_symbol = 'Ru'
    functional = 'b3lyp'
    basis_set = 'Def2SVP'
    charge = 0

    mol = read(xyz_file)
    mol.calc = Gaussian(label='single_point',
                        nprocshared=n_procs,
                        mem='4GB',
                        chk='single_point.chk',
                        xc=functional,
                        charge=charge,
                        mult=M,
                        basis=basis_set,
                        pop='Hirshfeld',
                        SCRF='Solvent=Water',
                        scf='tight')

    mol.get_potential_energy()
    return


def gaussian_sp_converged(log_file):
     with open(log_file) as log:
        if 'SCF Done' in log.read():
            print('\nSINGLE POINT SUCCESSFULLY PERFORMED\n')
            return True
        else:
            print('\nSINGLE POINT NOT SUCCESSFUL\n')
            return sys.exit()

