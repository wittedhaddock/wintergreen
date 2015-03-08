//
//  ViewController.m
//  wintergreen
//
//  Created by James Graham on 3/8/15.
//  Copyright (c) 2015 JamesGraham. All rights reserved.
//

#import "ViewController.h"
#import <CoreMotion/CoreMotion.h>

@interface ViewController () <NSCoding>
@property (strong, nonatomic) CMMotionManager *manager;

//gyro
@property (weak, nonatomic) IBOutlet UILabel *gX;
@property (weak, nonatomic) IBOutlet UILabel *gY;
@property (weak, nonatomic) IBOutlet UILabel *gZ;

//accel
@property (weak, nonatomic) IBOutlet UILabel *aX;
@property (weak, nonatomic) IBOutlet UILabel *aY;
@property (weak, nonatomic) IBOutlet UILabel *aZ;

@property (strong, nonatomic) NSMutableArray *aggregateData;

@end

@implementation ViewController

- (CMMotionManager *)manager{
    if(!_manager){
        _manager = [[CMMotionManager alloc] init];
    }
    return _manager;
}

- (NSMutableArray *)aggregateData{
    if (!_aggregateData) {
        _aggregateData = [NSMutableArray array];
    }
    return _aggregateData;
}

- (void)viewDidLoad {
    [super viewDidLoad];

    if ([self.manager isGyroAvailable] && [self.manager isGyroActive] == NO) {
        [self startGryoUpdate];
    }
    if ([self.manager isAccelerometerAvailable] && [self.manager isAccelerometerActive] == NO) {
        [self startAccelerometerUpdate];
    }
}

#pragma mark - GYROSCOPE
- (void)startGryoUpdate{
    [self.manager setGyroUpdateInterval:0.01f];
    [self.manager startGyroUpdatesToQueue:[NSOperationQueue mainQueue]
                              withHandler:^(CMGyroData *gyroData, NSError *error) {
                                  if (!error) {
                                      [self processGyroData:gyroData];
                                  }
                                  else {
                                      NSLog(@"ERROR:\n%@", [error userInfo]);
                                  }
                              }];
}
- (void)processGyroData:(CMGyroData *)data{
    double x = data.rotationRate.x;
    double y = data.rotationRate.y;
    double z = data.rotationRate.z;
    [self updateViewWithNewGyroDataX:x Y:y Z:z];
}

- (void)updateViewWithNewGyroDataX:(double)x Y:(double)y Z:(double)z{
    self.gX.text = [NSString stringWithFormat:@"X: %f", x];
    self.gY.text = [NSString stringWithFormat:@"Y: %f", y];
    self.gZ.text = [NSString stringWithFormat:@"Z: %f", z];
    
    
    
#warning what a terrible pattern this is...wonder how the mainQueue handles both data streams, and whether their invocation time can be mapped to real system time
    [self bundleData];
}

- (void)bundleData{
    NSString *gyro = [NSString stringWithFormat:@"%@, %@, %@", self.gX.text, self.gY.text, self.gZ.text];
    NSString *accel = [NSString stringWithFormat:@"%@, %@, %@", self.aX.text, self.aY.text, self.aZ.text];
    NSString *amalgamate = [NSString stringWithFormat:@"G: %@ A: %@ D: %@", gyro, accel, [NSDate date]];
    [self.aggregateData addObject:amalgamate];
}

#pragma mark - ACCELEROMETER

- (void)startAccelerometerUpdate{
    [self.manager setAccelerometerUpdateInterval:0.01f];
    [self.manager startAccelerometerUpdatesToQueue:[NSOperationQueue mainQueue]
                                       withHandler:^(CMAccelerometerData *accelerometerData, NSError *error) {
                                           if (!error) {
                                               [self processAccelData:accelerometerData];
                                           }
                                           else {
                                               NSLog(@"ERROR:\n%@", [error userInfo]);
                                           }
    }];
}

- (void)processAccelData:(CMAccelerometerData *)data{
    double x = data.acceleration.x;
    double y = data.acceleration.y;
    double z = data.acceleration.z;
    [self updateViewWithNewAccelDataX:x Y:y Z:z];
}

- (void)updateViewWithNewAccelDataX:(double)x Y:(double)y Z:(double)z{
    self.aX.text = [NSString stringWithFormat:@"X: %f", x];
    self.aY.text = [NSString stringWithFormat:@"Y: %f", y];
    self.aZ.text = [NSString stringWithFormat:@"Z: %f", z];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - ENCODING
#define GYRO_ROTATION_RATE_X_KEY @"gX"
#define GYRO_ROTATION_RATE_Y_KEY @"gY"
#define GYRO_ROTATION_RATE_Z_KEY @"gZ"

#define ACCEL_ACCELERATION_X_KEY @"aX"
#define ACCEL_ACCELERATION_Y_KEY @"aY"
#define ACCEL_ACCELERATION_Z_KEY @"aZ"

- (BOOL)createDataPath {
    

    
    NSError *error;
    BOOL success = [[NSFileManager defaultManager] createDirectoryAtPath:@"./" withIntermediateDirectories:YES attributes:nil error:&error];
    if (!success) {
        NSLog(@"Error creating data path: %@", [error localizedDescription]);
    }
    return success;
    
}

- (void)saveData {
    
    [self createDataPath];
    
    NSString *dataPath = @"./data.plist";
    for (NSString *indexer in self.aggregateData) {
        NSMutableData *data = [[NSMutableData alloc] initWithData:[indexer dataUsingEncoding:NSUTF8StringEncoding]];
        NSKeyedArchiver *archiver = [[NSKeyedArchiver alloc] initForWritingWithMutableData:data];
        [archiver finishEncoding];
        [data writeToFile:dataPath atomically:YES];
    }
}

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event{
    [self saveData];
}

@end
