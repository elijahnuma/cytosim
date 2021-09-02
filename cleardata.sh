# deletes all plots except for diffusion
find ./csvs/ -not -path "./csvs/diffusion*" -name "*.csv" -type f -delete
find ./plots/ -not -path "./plots/diffusion*" -name "*.png" -type f -delete
