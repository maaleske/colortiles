import xarray as xr
import sys


def main(argv):
    inputfile = argv[0]
    output = argv[1]
    variable = argv[2]

    print(f'Calculating reflectances from dataset {inputfile}')
    print(f'and saving result to {output}.')
    print(80*'=')
    print('Reading dataset')
    ds = xr.open_dataset(inputfile)
    ds.load()

    refs = ds.where(ds.material == 'White', drop=True)
    print(f'Calculating reflectances using references {refs.time.values}')
    refls = []
    for t, ref in refs.groupby('time'):
        print(f'Reference {t}')
        refl = ds[variable] / ref[variable]
        refl.coords['reference'] = t
        refls.append(refl)

    print(f'Saving results to {output}')
    ds['reflectance'] = xr.concat(refls, dim='reference')
    ds = ds.drop(variable)
    ds.to_netcdf(output)


if __name__ == '__main__':
    main(sys.argv[1:])