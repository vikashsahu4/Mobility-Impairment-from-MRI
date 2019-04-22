from radiomics import featureextractor
import SimpleITK as sitk
import json

#imageName = os.path.join(dataDir, "data", 'sample.nrrd')
#maskName = os.path.join(dataDir, "data",  'smp.nrrd')
#imageName="sample.nrrd"
#maskName="sample_label.nrrd"
imageName="output_all_fast_firstseg.nii"

#Load MRI image data from ITK
img = sitk.ReadImage(imageName)


#casting the image so that the pixel dimesions all match with each other
img_mask = sitk.Cast(img , sitk.sitkUInt8)
img = sitk.Cast(img, sitk.sitkFloat32)
corrector = sitk.N4BiasFieldCorrectionImageFilter()

#corrector is used so that there is an equation of the dimensions
img_c = corrector.Execute(img, img_mask)
#img_c = corrector.Execute(img)

#params = os.path.join(dataDir, "bin", "Params.yaml")
#specify the parameters for the program to execute(Pyradiomics)
params="Params.yaml"

#Setting up model to extract features
extractor = featureextractor.RadiomicsFeaturesExtractor(params)

#check configuration 
print('Extraction parameters:\n\t', extractor.settings)
print('Enabled filters:\n\t', extractor._enabledImagetypes)
print('Enabled features:\n\t', extractor._enabledFeatures)

#Function to save json file
def save(dic,name):
    output=name+'.json'
    with open(output, 'w') as outfile:
        json.dump(thalamus, outfile)
    
#Hippocampus ROI
hippocampus = extractor.execute(img, img_mask, label=53)

#Thalamus
thalamus=extractor.execute(img, img_mask, label=10)
with open('thalamus.json', 'w') as outfile:
    json.dump(thalamus, outfile)
    
#Sample output 
print('Result type:', type(thalamus))  # result is returned in a Python ordered dictionary)
print('')
print('Calculated features for Label 6')
for key, value in thalamus.items():
    print('\t', key, ':', value)

#Caudate
caudate=extractor.execute(img, img_mask, label=11)

#Putamen
putamen=extractor.execute(img, img_mask, label=12)

#Pallidum
pallidum=extractor.execute(img, img_mask, label=13)




